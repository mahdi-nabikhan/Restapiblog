import AddPosts from "./Components/AddPosts/AddPosts"
import AboutUs from "./Components/Main/AboutUs/AboutUs"
import ContactUs from "./Components/Main/ContactUs/ContactUs"
import PostDetail from "./Components/Main/PostDetail/PostDetail"
import Profile from "./Components/Panel/Profile/Profile"
import ProfileUpdate from "./Components/Panel/ProfileUpdate/ProfileUpdate"
import MainLayout from "./Layouts/MainLayout"
import ProfileLayout from "./Layouts/ProfileLayout"
import Login from "./Pages/Login/Login"
import Index from "./Pages/Main/Index/Index"
import PostDetailPages from "./Pages/Main/PostDetailPages/PostDetailPages"
import Panel from "./Pages/Panel/Panel"
import PostUpdatePage from "./Pages/PostUpdate/PostUpdatePage"
import PostUpdate from "./Pages/PostUpdate/PostUpdatePage"
import ProfilePage from "./Pages/ProfilePage/ProfilePage"
import Register from "./Pages/Register/Register"
import UpdateProfilePage from "./Pages/UpdateProfilePage/UpdateProfilePage"


const routes = [{
    path: '/', element: <MainLayout />, children: [
        { index: true, element: <Index /> },
        { path: 'login', element: <Login /> },
        { path: 'register', element: <Register /> },
        { path: 'post/:id', element: <PostDetailPages /> },
        { path: 'add/post', element: <AddPosts /> },
        { path: 'about/us', element: <AboutUs /> },
        { path: 'contact/us', element: <ContactUs /> }

    ],
},
{
    path: '/panel', element: <ProfileLayout />, children: [
        { index: true, element: <Panel /> },
        { path: 'post/:id', element: <PostUpdatePage /> },
        { path: 'profile/edit', element: <UpdateProfilePage /> },
        { path: 'profile/detail', element: <ProfilePage /> }

    ]
},
{
    path: "*",
    element: <NotFound />,
},

]


export default routes