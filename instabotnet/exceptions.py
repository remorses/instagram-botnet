# try random network request, if fail
NetworkException

# exception based on http codes
{
   429: ThrottledException('Throttled by Instagram because of too many API requests.'),
   431: RequestHeadersTooLargeException('The request start-line and/or headers are too large to process.'),
   400: BadRequestException,
   404: NotFoundException,
   _: EmptyResponseException, # when response from instagram is empty
}

# all instagram responses return exceptions inside a message property
{
        /*
         * Whether the API request succeeded or not.
         *
         * Can be: "ok", "fail".
         */
        'status'  : 'string',
        /*
         * Instagram's API failure error message(s).
         *
         * NOTE: This MUST be marked as 'mixed' since the server can give us
         * either a single string OR a data structure with multiple messages.
         * Our custom `getMessage()` will take care of parsing their value.
         */
        'message' : 'string' | {'errors': []},
        /*
         * This can exist in any Instagram API response, and carries special
         * status information.
         *
         * Known messages: "fb_needs_reauth", "vkontakte_needs_reauth",
         * "twitter_needs_reauth", "ameba_needs_reauth", "update_push_token".
         */
        '_messages' : 'Response\Model\_Message[]',
}
    


# exceptions based on message and error_type
# some endpoins like `login`, `users/check_username`, `users/check_email` returns an {error_type: ...} property,
# others return {message: {errors: [...]}}
# all direct send item istead returns {payload: {
        'client_request_id' : 'string',
        'client_context'    : 'string',
        'message'           : 'string', # error message here
        'item_id'           : 'string',
        'timestamp'         : 'string',
        'thread_id'         : 'string',
        'canonical'         : 'bool',
        'participant_ids'   : 'string[]'
}


EXCEPTION_MAP = {
        'LoginRequiredException'       : ['login_required'],
        'CheckpointRequiredException'  : [
            'checkpoint_required', // message
            'checkpoint_challenge_required', // error_type
        ],
        'ChallengeRequiredException'   : ['challenge_required'],
        'FeedbackRequiredException'    : ['feedback_required'],
        'ConsentRequiredException'     : ['consent_required'],
        'IncorrectPasswordException'   : [
            // "The password you entered is incorrect".
            '/password(.*?)incorrect/', // message
            'bad_password', // error_type
        ],
        'InvalidSmsCodeException'      : [
            // "Please check the security code we sent you and try again".
            '/check(.*?)security(.*?)code/', // message
            'sms_code_validation_code_invalid', // error_type
        ],
        'AccountDisabledException'     : [
            // "Your account has been disabled for violating our terms".
            '/account(.*?)disabled(.*?)violating/',
        ],
        'SentryBlockException'         : ['sentry_block'],
        'InvalidUserException'         : [
            // "The username you entered doesn't appear to belong to an account"
            '/username(.*?)doesn\'t(.*?)belong/', // message
            'invalid_user', // error_type
        ],
        'ForcedPasswordResetException' : ['/reset(.*?)password/'],
}




    