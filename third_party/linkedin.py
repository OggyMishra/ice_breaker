import os
import requests
from dotenv import load_dotenv


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from linkedin profile"""
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        load_dotenv()
        headers = {"Authorization": "Bearer " + os.environ.get("PROXYCURL_API_KEY")}
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        params = {"linkedin_profile_url": linkedin_profile_url}
        response = requests.get(
            api_endpoint, params=params, headers=headers, timeout=10
        )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data


# if __name__ == "__main__":
#     load_dotenv()
#     linkedin_profile_url = "https://www.linkedin.com/in/sourabh-mishra-8a815998"
#     res = scrape_linkedin_profile(linkedin_profile_url)
#     print(res)
