import {
  useQuery,
  useMutation,
  useQueryClient,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import ErrorBoundary from './ErrorBoundary';
import './App.css';
import { useRoutes } from 'react-router-dom';
import routes from './routes';
const queryClient = new QueryClient({
  defaultOptions:{
    queries:{
      gcTime:50000,
      staleTime:10000,
      retry:false,
      refetchInterval:3000,
      
    }
    
  }
})
function App() {
  
  const router = useRoutes(routes)
  return (
    <><ErrorBoundary><QueryClientProvider client={queryClient}>
      {router}
    </QueryClientProvider>
      </ErrorBoundary>
    
    </>
  );
}

export default App;
