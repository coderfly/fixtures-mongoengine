# -*- coding: utf-8 -*-

fixture_data = {
    'post1': {
        'title': 'Sherlock Gets A Musical Parody',
        'text': 'Sherlock fans still have a way to go before Season 4 of the BBC drama finally arrives.',
        'author': '{users.user1}',
    },
    'post2': {
        'title': 'NASA prepares to sample an asteroid',
        'text': 'On September 8, NASA will launch its first sample return mission to an asteroid.',
        'author': '{users.user2}',
    }
}

fixture_data_embedded = {
    'post1': {
        'title': 'Sherlock Gets A Musical Parody',
        'text': 'Sherlock fans still have a way to go before Season 4 of the BBC drama finally arrives.',
        'author': {
            'id': '{users.user1}',
            'first_name': 'Joyce',
            'last_name': 'Ray'
        },
    },
    'post2': {
        'title': 'NASA prepares to sample an asteroid',
        'text': 'On September 8, NASA will launch its first sample return mission to an asteroid.',
        'author': {
            'id': '{users.user2}',
            'first_name': 'Amy',
            'last_name': 'Myers'
        },
    }
}

fixture_data_wrong_ref_format = {
    'post1': {
        'title': 'Sherlock Gets A Musical Parody',
        'text': 'Sherlock fans still have a way to go before Season 4 of the BBC drama finally arrives.',
        'author': '{users}',
    }
}

fixture_data_wrong_ref = {
    'post1': {
        'title': 'Sherlock Gets A Musical Parody',
        'text': 'Sherlock fans still have a way to go before Season 4 of the BBC drama finally arrives.',
        'author': '{users.wrong_user_ref}',
    }
}
