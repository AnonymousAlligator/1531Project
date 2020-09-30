                    if u_id in channel['owner_members']:
                        for owner in channels['owner_members']:
                            if u_id == owner['uid']:
                                channels['owner_members'].remove(owner)