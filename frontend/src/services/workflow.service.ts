import axios from 'axios';
import config from '../config';

interface WorkflowRequest {
    user_query: string;
    table_id: string;
}

interface WorkflowResponse {
    answer: string;
    visualization: any;
    visualization_reason: string;
    formatted_data_for_visualization: any;
    // Add any other response properties from the backend
}

export const workflowAPI = async (query: string, tableId: string): Promise<WorkflowResponse> => {
    try {
        const response = await axios.post<WorkflowResponse>(
            `${config.backendUrl}/analyze/query`,
            {
                user_query: query,
                table_id: tableId
            } as WorkflowRequest
        );
        
        console.log(response.data);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw new Error(error.response?.data?.detail || 'Failed to process query');
        }
        throw error;
    }
}