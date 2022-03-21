from pymongo import MongoClient
from settings import MONGO_DB, MONGODB_LINK

mdb = MongoClient(MONGODB_LINK)[MONGO_DB]

def search_or_save_user(mdb, effective_user, message):
    user = mdb.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "chat_id": message.chat.id,
            "vote_results_number": 0
        }
        mdb.users.insert_one(user)
    return user

def save_user_vote(mdb, user, user_data):
    mdb.users.update_one(
        {'_id': user['_id']},
        {'$set': {"vote_results_number": user["vote_results_number"]+1}}
    )
    if 'vote_results' not in user:
         hist1 = user_data['hist1']
         hist2 = user_data['hist2']
         Sim = user_data['Sim']
         NonSim = user_data['NonSim']
         Dont = user_data['Dont Know']
         Date = user_data['Date']
         Time = user_data['Time']
    else:
        hist1 = user['vote_results']['hist1']
        hist2 = user['vote_results']['hist2']
        Sim = user['vote_results']['Sim']
        NonSim = user['vote_results']['NonSim']
        Dont = user['vote_results']['Dont Know']
        Date = user['vote_results']['Date']
        Time = user['vote_results']['Time']

        hist1.extend(user_data['hist1'])
        hist2.extend(user_data['hist2'])
        Sim.extend(user_data['Sim'])
        NonSim.extend(user_data['NonSim'])
        Dont.extend(user_data['Dont Know'])
        Date.extend(user_data['Date'])
        Time.extend(user_data['Time'])

    mdb.users.update_one(
             {'_id': user['_id']},
             {'$set':{'vote_results': {'hist1': hist1,
                                       'hist2': hist2,
                                       'Sim': Sim,
                                       'NonSim': NonSim,
                                       'Dont Know': Dont,
                                       'Date': Date,
                                       'Time': Time
                                       }
                      }
              }
    )
    return user