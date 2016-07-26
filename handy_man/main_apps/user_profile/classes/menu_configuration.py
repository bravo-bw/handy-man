from ...main.constants import (
    MY_PROFILE, ARTISAN, CUSTOMER, SME, POST_JOB, USERS, HANDYMAN_ADMIN, AVAILABLE_JOBS,
    DASHBOARD, JOBS_COMPLETED, JOBS_IN_PROGRESS, SERVICE, CONTACT_US, ADD_JOB, NOTIFICATIONS)


class MenuConfiguration:

    # TODO: Consider making these configurable as database records, but be carefull of performance penalty of having
    # to query DB for menus at every request to server
    def user_menu_list(self, user_profile):
        title, url_name, para = DASHBOARD
        DASHBOARD_DATA = (title, url_name, user_profile.user.username)
        if not user_profile.account_type:
            return [MY_PROFILE]
        elif user_profile.account_type == ARTISAN:
            return [[DASHBOARD_DATA], self.jobs, [NOTIFICATIONS], [SERVICE], [CONTACT_US]]
        elif user_profile.account_type == CUSTOMER:
            return [[DASHBOARD_DATA], self.customer_jobs, [NOTIFICATIONS], [USERS], [SERVICE], [CONTACT_US]]
        elif user_profile.account_type == SME:
            return [[USERS], [POST_JOB], [NOTIFICATIONS], [SERVICE], [CONTACT_US]]
        elif user_profile.account_type == HANDYMAN_ADMIN:
            return [[MY_PROFILE], [AVAILABLE_JOBS], [NOTIFICATIONS], [USERS], [SERVICE], [CONTACT_US]]

    @property
    def jobs(self):
        return [('Jobs', 'available_url'), [JOBS_IN_PROGRESS, AVAILABLE_JOBS, JOBS_COMPLETED]]

    @property
    def customer_jobs(self):
        return [('Jobs', 'available_url'), [ADD_JOB, JOBS_IN_PROGRESS, JOBS_COMPLETED]]
