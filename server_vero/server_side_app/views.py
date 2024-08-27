import io
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .baubuddy_api import BaubuddyAPI


def decode_file(file):
    # Read the CSV content
    try:
        # Decode the file content from bytes to a string
        decoded_file = file.read().decode('utf-8')

        # Use StringIO to treat the string as a file object for pandas
        csv_data = pd.read_csv(io.StringIO(decoded_file), sep=None, engine='python')
        return csv_data
    except Exception as e:
        print (JsonResponse({"error": f"Error reading CSV file: {e}"}, status=400))
        return None


@csrf_exempt
@api_view(['POST'])
def upload_csv(request):
    # Parse the uploaded file
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({"error": "No file uploaded."}, status=400)

    csv_data = decode_file(file)  # decode for python script

    # Get access token for authorization
    exterbal_api_manager = BaubuddyAPI()
    if not exterbal_api_manager.token_available():
        return JsonResponse({"error": "Failed to get token."}, status=500)

    # Fetch additional vehicle data from the external API
    api_data = exterbal_api_manager.fetch_vehicle_data()

    # Convert the API response to a DataFrame
    api_df = pd.DataFrame(api_data)

    # Merge CSV data with the external API data
    combined_df = pd.concat([csv_data, api_df], ignore_index=True).drop_duplicates()

    # Filter out rows where 'hu' field is missing
    combined_df = combined_df[combined_df['hu'].notna()]

    # Resolve color codes for labelIds
    combined_df['colorCodes'] = combined_df['labelIds'].apply(lambda x: exterbal_api_manager.resolve_color_codes(x) if pd.notna(x) else [])

    # Convert the result to JSON format
    result = combined_df.to_dict(orient="records")
    return JsonResponse(result, safe=False)

