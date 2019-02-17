"""
    instabot example
    Workflow:
        Save users' following into a file.
"""
from memory_profiler import profile


from instabotnet.api import API

@profile
def main():
    api = API()
    api.login(username='__morse', password='ciuccio99',)
    following = api.get_profile_data()
    following = api.get_profile_data()
    following = api.get_profile_data()
    following = api.get_profile_data()

main()
