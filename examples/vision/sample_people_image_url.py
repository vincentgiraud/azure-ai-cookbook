import os
from dotenv import load_dotenv

load_dotenv()

def sample_people_image_url():
    import os
    from azure.ai.vision.imageanalysis import ImageAnalysisClient
    from azure.ai.vision.imageanalysis.models import VisualFeatures
    from azure.core.credentials import AzureKeyCredential

    # Set the values of your computer vision endpoint and computer vision key
    # as environment variables:
    try:
        endpoint = os.getenv("VISION_ENDPOINT")
        key = os.getenv("VISION_KEY")
    except KeyError:
        print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
        print("Set them before running this sample.")
        exit()

    # Create an Image Analysis client
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # [START caption]
    # Get a caption for the image. This will be a synchronously (blocking) call.
    result = client.analyze_from_url(
        image_url=os.getenv("IMAGE_URL"),
        visual_features=[VisualFeatures.PEOPLE, VisualFeatures.TAGS],
        gender_neutral_caption=True,  # Optional (default is False)
    )

    # Print results
    print("Image analysis results:")
    print(f" Image height: {result.metadata.height}")
    print(f" Image width: {result.metadata.width}")
    print(f" Model version: {result.model_version}")
    if result.people is not None:
        people_count = 0
        for person in result.people.list:
            if person.confidence > 0.9:
                people_count += 1 
        if people_count == 0:
            print(" No people detected in the image.")
        else:
            print(f" {people_count} people detected in the image.")

if __name__ == "__main__":
    sample_people_image_url()
