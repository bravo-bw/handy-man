from ...main.constants import MY_PROFILE, HOME, ARTISAN, CUSTOMER, SME, JOBS, POST_JOB, USERS, HANDYMAN_ADMIN, AVAILABLE_JOBS


class MenuConfiguration:

    # TODO: Consider making these configurable as database records, but be carefull of performance penalty of having
    # to query DB for menus at every request to server
    def user_menu_list(self, user_profile):
        if not user_profile.account_type:
            return [HOME, MY_PROFILE]
        elif user_profile.account_type == ARTISAN:
            return [HOME, MY_PROFILE, JOBS, AVAILABLE_JOBS, USERS]
        elif user_profile.account_type == CUSTOMER:
            return [HOME, MY_PROFILE, USERS, POST_JOB]
        elif user_profile.account_type == SME:
            return [HOME, MY_PROFILE, JOBS, USERS, POST_JOB]
        elif user_profile.account_type == HANDYMAN_ADMIN:
            return [HOME, MY_PROFILE, JOBS, AVAILABLE_JOBS, USERS]
