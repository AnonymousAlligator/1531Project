from auth import auth_register

def create_one_test_user():
    # Register 1 users
    return auth_register("test_email_0@email.com", "valid_pw0", "Hayden", "Jacobs")

def create_two_test_users():
    # Register 2 users
        test_user_0 = auth_register("test_email_0@email.com", "valid_pw0", "Hayden", "Jacobs")
        test_user_1 = auth_register("test_email_1@email.com", "valid_pw1", "Jayden", "Haycobs")

        return test_user_0, test_user_1

def create_three_test_users():
    # Register 3 users
        test_user_0 = auth_register("test_email_0@email.com", "valid_pw0", "Hayden", "Jacobs")
        test_user_1 = auth_register("test_email_1@email.com", "valid_pw1", "Jayden", "Haycobs")
        test_user_3 = auth_register("test_email_2@email.com", "valid_pw1", "Nick", "Smith")

        return test_user_0, test_user_1, test_user_3


# TODO: Potentially add channel helpers