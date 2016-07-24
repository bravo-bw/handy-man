from ...main.constants import (
    MY_PROFILE, ARTISAN, CUSTOMER, SME, POST_JOB, USERS, HANDYMAN_ADMIN, AVAILABLE_JOBS, 
    DASHBOARD, JOBS_COMPLETED, JOBS_IN_PROGRESS, SERVICE, CONTACT_US)


class MenuConfiguration:

    # TODO: Consider making these configurable as database records, but be carefull of performance penalty of having
    # to query DB for menus at every request to server
    def user_menu_list(self, user_profile):
        if not user_profile.account_type:
            return [MY_PROFILE]
        elif user_profile.account_type == ARTISAN:
            return [self.jobs, [SERVICE], [CONTACT_US]]
        elif user_profile.account_type == CUSTOMER:
            title, url_name, para = DASHBOARD
            DASHBOARD_DATA = (title, url_name, user_profile.user.username)
            return [[DASHBOARD_DATA], [USERS], [POST_JOB], [SERVICE], [CONTACT_US]]
        elif user_profile.account_type == SME:
            return [[USERS], [POST_JOB], [SERVICE], [CONTACT_US]]
        elif user_profile.account_type == HANDYMAN_ADMIN:
            return [[MY_PROFILE], [AVAILABLE_JOBS], [USERS], [SERVICE], [CONTACT_US]]

    @property
    def jobs(self):
        return [('Jobs', 'available_url'), [AVAILABLE_JOBS, JOBS_IN_PROGRESS, JOBS_COMPLETED]]
