import {
  useQuery,
  useMutation,
  useQueryClient,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import './App.css';
import { useRoutes } from 'react-router-dom';
import routes from './routes';
const queryClient = new QueryClient({
  defaultOptions:{
    queries:{
      gcTime:5000,
      staleTime:10000
    }
    
  }
})
function App() {
  
  const router = useRoutes(routes)
  return (
    <><QueryClientProvider client={queryClient}>
      {router}
    </QueryClientProvider>
    
    </>
  );
}

export default App;
