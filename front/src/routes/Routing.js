import { Routes, Route } from 'react-router-dom';
import MainPage from "../MainPage/Main";
import NewPage from "../NewPage/New"
import NewsByTag from "../NewsByTag/NewsByTag"

export default function MembersRouter() {
    return (
        <Routes>
            <Route path="/" element={<MainPage />} />
            <Route path="*" element={null} />
            <Route path="new/:id" element={<NewPage />} />
            <Route path="tag/:id" element={<NewsByTag/>} />
        </Routes>
    )
}
         