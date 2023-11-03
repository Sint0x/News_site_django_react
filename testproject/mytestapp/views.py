from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers, status
from .models import News,NewsImages,Anonymous,AnonymousFeedback, NewTags
from .serializers import NewsSerializer
import time
import secrets

class NewViews:

    @staticmethod
    @api_view(['GET'])
    def getall(request):
        page_number = int(request.GET.get('page', 1))  # Получаем номер страницы из запроса
        page_size = 3  # Устанавливаем количество товаров на страницу
        offset = (page_number - 1) * page_size  # Вычисляем смещение

        # Получить новости, отсортированные по ID в порядке убывания, с учетом пагинации
        news_list = News.objects.all().order_by('-id')[offset:offset+page_size]
        serializer = NewsSerializer(news_list, many=True)
        news_data = serializer.data

        # Для каждой новости получить изображения и добавить их в ответ
        for news in news_data:
            images = NewsImages.objects.filter(news_id=news['id']).values_list('image', flat=True)
            news['images'] = list(images)

        for news in news_data:
            tags = NewTags.objects.filter(news_id=news['id']).values('tag__id', 'tag__tag')
            news['tags'] = {tag['tag__id']: tag['tag__tag'] for tag in tags}
            
        return Response({
            'amount': News.objects.count(),
            'page_size': page_size,
            'results': news_data
        }, status=status.HTTP_200_OK) 
    
    @api_view(['POST'])
    def post(request):
        # Начать новую транзакцию
        with transaction.atomic():
            # Сначала сохранить новость
            serializer = NewsSerializer(data=request.data)
            if serializer.is_valid():
                news = serializer.save()
            else:
                return Response(serializer.errors, status=400)

            # Затем сохранить изображения
            images = request.FILES.getlist('images')
            if images and len(images) <= 10:  
                path = '../front/src/images'
                file_storage = FileSystemStorage(location=path)
                print(file_storage)


                for image in images:
                    unix_time = int(time.time())
                    image_name = file_storage.save(f'{unix_time}.jpg', ContentFile(image.read()))
                    news_image = NewsImages(news=news, image=image_name)
                    news_image.save()

        return Response(status=201)


    @api_view(['GET'])
    def getone(request,id):
        new = News.objects.get(id=id)
        serializer = NewsSerializer(new)
        result = serializer.data

        images = NewsImages.objects.filter(news_id=result['id']).values_list('image', flat=True)
        result['images'] = list(images)


        views = AnonymousFeedback.objects.filter(news_id=id).count()
        likes = AnonymousFeedback.objects.filter(news_id=id,rate = 1).count()
        dislikes = AnonymousFeedback.objects.filter(news_id=id,rate = 0).count()
        result['views_count'] = views
        result['likes_count'] = likes
        result['dislikes_count'] = dislikes
        tags = NewTags.objects.filter(news_id=result['id']).values('tag__id', 'tag__tag')
        result['tags'] = {tag['tag__id']: tag['tag__tag'] for tag in tags}

        return Response(result)
        
    @api_view(['DELETE'])
    def delete(request,id):
        new = News.objects.filter(id=id).delete()

        return Response(status=202)
    
    @api_view(['PUT'])
    def update(request,id):
        new = News.objects.filter(id=id).update(**request.data)

        return Response(status=201)
    

class FeedBackView:

    @api_view(['POST'])
    def feedupdateorcreate(request):


        def createFeedBack(anonymousId, newsId, rateNum):
            AnonymousFeedback.objects.create(anonymous_id=anonymousId, news_id=newsId, rate=rateNum)
        # Извлекаем оценку и ID новости из данных запроса
        rate = request.data.get('rate')
        new_id = request.data.get('new_id')

        # Извлекаем токен из заголовков запроса
        token = request.headers.get('FeedBack')

        # Если токен отсутствует, создаем новый анонимный объект с уникальным токеном
        if not token:
            token = secrets.token_hex(32)
            Anonymous.objects.create(token = token)
            anonymous = Anonymous.objects.get(token=token)
            createFeedBack(anonymous.id, new_id, rate)

            # Возвращаем ответ с оценкой и токеном, статус 201 означает "Создано"
            return Response({'rate': rate,'FeedBack':token}, status=201)

        # Если токен присутствует, получаем соответствующий анонимный объек
    
        anonymous = Anonymous.objects.get(token=token)

        # Проверяем, существует ли уже отзыв для данного анонимного пользователя и новости
        feedback = AnonymousFeedback.objects.filter(anonymous_id=anonymous.id, news_id=new_id).last()

        # Если отзыв уже существует и его оценка не равна переданной оценке,
        # возвращаем ответ с сообщением об ошибке, статус 403 означает "Запрещено"
        if feedback.rate == 1 or feedback.rate == 0:

        # Если отзыв уже существует и его оценка равна переданной оценке,
        # обновляем оценку и сохраняем изменения в базе данных,
        # затем возвращаем ответ с сообщением об успешном изменении оценки
            if feedback.rate != rate:
                feedback.rate = rate
                feedback.save()
                return Response({'rate': rate, 'message':'Оценка изменена'},status=201)
            
            return Response({'message': 'Пост уже оценен вами'}, status=403)

        # Если отзыв не существует, создаем новый отзыв
        createFeedBack(anonymous.id, new_id, rate)

        # Возвращаем ответ с оценкой, статус 201 означает "Создано"
        return Response({'rate': rate}, status=201)


    @api_view(['POST'])
    def viewsupdate(request):
        newId = request.data.get('new_id')
        token = request.headers.get('FeedBack')

        if token == 'null':
            print(token)
            token = secrets.token_hex(32)
            Anonymous.objects.create(token=token)
        anonymous = Anonymous.objects.get(token=token)
        feedback = AnonymousFeedback.objects.filter(anonymous_id=anonymous.id, news_id=newId).first()
        if feedback is None:
            feedback = AnonymousFeedback.objects.create(anonymous_id=anonymous.id, news_id=newId)

        if feedback.status == 1:
            return Response({'FeedBack':token},status=403)
        else:
            feedback.status = 1
            feedback.save()
            return Response({'FeedBack':token}, status=201)
        
class NewsByTagView():
    @api_view(['GET'])
    def get(request, id):
        page_number = int(request.GET.get('page', 1))  # Получаем номер страницы из запроса
        page_size = 3  # Устанавливаем количество товаров на страницу
        offset = (page_number - 1) * page_size  # Вычисляем смещение
        new_tags = NewTags.objects.filter(tag_id=id)
        news_ids = new_tags.values_list('news', flat=True)
        news = News.objects.filter(id__in=news_ids).order_by('-id')[offset:offset+page_size]
        serializer = NewsSerializer(news, many=True)
        news_data = serializer.data

        for news in news_data:
            images = NewsImages.objects.filter(news_id=news['id']).values_list('image', flat=True)
            news['images'] = list(images)

        for news in news_data:
            tags = NewTags.objects.filter(news_id=news['id']).values('tag__id', 'tag__tag')
            news['tags'] = {tag['tag__id']: tag['tag__tag'] for tag in tags}

        return Response({
            'amount': News.objects.filter(id__in=news_ids).count(),
            'page_size': page_size,
            'results': news_data
        }, status=status.HTTP_200_OK)
