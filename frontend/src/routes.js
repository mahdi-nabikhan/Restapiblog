import AddPosts from "./Components/AddPosts/AddPosts"
import PostDetail from "./Components/Main/PostDetail/PostDetail"
import Profile from "./Components/Panel/Profile/Profile"
import MainLayout from "./Layouts/MainLayout"
import ProfileLayout from "./Layouts/ProfileLayout"
import Login from "./Pages/Login/Login"
import Index from "./Pages/Main/Index/Index"
import PostDetailPages from "./Pages/Main/PostDetailPages/PostDetailPages"
import Register from "./Pages/Register/Register"


const routes = [{
    path:'/' , element:<MainLayout/>,    children: [
        { index: true, element: <Index/> },
        { path: 'login', element: <Login /> },
        { path: 'register', element: <Register /> },
        {path:'post/:id',element:<PostDetailPages/>},
        {path:'add/post',element:<AddPosts/>}
      ],
},
{path :'/panel',element:<ProfileLayout/>,children:[
          {path:'profile',element:<Profile/>},

]}]


export default routes