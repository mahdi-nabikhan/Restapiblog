import MainLayout from "./Layouts/MainLayout"
import ProfileLayout from "./Layouts/ProfileLayout"
import Login from "./Pages/Login/Login"
import Index from "./Pages/Main/Index/Index"
import Register from "./Pages/Register/Register"


const routes = [{
    path:'/' , element:<MainLayout/>,    children: [
        { index: true, element: <Index/> },
        { path: 'login', element: <Login /> },
        { path: 'register', element: <Register /> },
      ],
},
{path :'/panel',element:<ProfileLayout/>,children:[

]}]


export default routes