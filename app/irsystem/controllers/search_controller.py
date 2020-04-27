from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.podcasts import Podcasts
from app.irsystem.controllers.similarity_calculator import *
from sqlalchemy.orm import load_only

project_name = "Find the Pea to your Podcast"
net_id = "Will Spencer: wes229, Theresa Cho: tsc82, Kathleen Xu: klx2, Yvonne Chan: yc686, Akira Shindo: as2568"


@irsystem.route('/', methods=['GET'])
def search():
	# queries all podcasts names
	query_podcast_names = Podcasts.query.order_by(Podcasts.name).options(load_only("name")).all()
	podcast_names = []
	for result in query_podcast_names:
		podcast_names.append(result.name)
	# print(all_podcast_names)

	# user input query
	query = request.args.get('podcast_search')

	if not query:
		data_dict_list = []
	else:
		#formatting list of podcast dicts
		query_all_podcasts = Podcasts.query.all()
		all_podcasts = []
		for result in query_all_podcasts:
			pod_dict = {
				'name': result.name,
				'description': result.description,
				'episode_count': result.ep_count,
				'avg_episode_duration': result.ep_durations,
				'link': result.itunes_url,
				'rating': result.rating
			}
			if result.artwork != "None":
				pod_dict['pic'] = result.artwork
			else:
				pod_dict['pic'] = "placeholder.jpg"

			pod_dict['genres'] = (result.genres).split(';')
			all_podcasts.append(pod_dict)
		# print(all_podcasts[0])

		query_podcast_info = Podcasts.query.filter_by(name=query).first_or_404()
		
		query_dict = {
			'name': query_podcast_info.name,
			'description': query_podcast_info.description,
			'episode_count': query_podcast_info.ep_count,
			'avg_episode_duration': query_podcast_info.ep_durations,
			'link': query_podcast_info.itunes_url,
			'rating': query_podcast_info.rating
		}
		if query_podcast_info.artwork != "None":
			query_dict['pic'] = query_podcast_info.artwork
		else:
			query_dict['pic'] = "placeholder.jpg"

		query_dict['genres'] = (query_podcast_info.genres).split(';')
		
		# formatting list of podcast reviews dicts for query
		all_reviews = []
		review_dict_1 = {
			'pod_name': result.name,
			'rev_text': result.review_1,
			'rev_rating': result.score_1
			}
		all_reviews.append(review_dict_1)
		review_dict_2 = {
			'pod_name': result.name,
     	'rev_text': result.review_2,   	     
			'rev_rating': result.score_2
    }
		all_reviews.append(review_dict_2)
		review_dict_3 = {
      'pod_name': result.name,
      'rev_text': result.review_3,
      'rev_rating': result.score_3
    }
		all_reviews.append(review_dict_3)
		review_dict_4 = {
    	'pod_name': result.name,
      'rev_text': result.review_4,
      'rev_rating': result.score_4
    }
		all_reviews.append(review_dict_4)
		review_dict_5 = {
      'pod_name': result.name,
      'rev_text': result.review_5,
      'rev_rating': result.score_5
    }
		all_reviews.append(review_dict_5)

		# print(all_reviews[0])

		# calculates similarity scores
		data_dict_list = get_ranked_podcast(query_dict, all_podcasts, all_reviews)

		# data_dict_list = [{
		# "pic": "http://is1.mzstatic.com/image/thumb/Music118/v4/8e/52/e1/8e52e12c-1bf4-0d48-8aeb-97d7a0c55582/source/100x100bb.jpg",
		# "name": "Myths and Legends",
		# "description": "Jason Weiser tells stories from myths, legends, and folklore that have shaped cultures throughout history. Some, like the stories of Aladdin, King Arthur, and Hercules are stories you think you know, but with surprising origins. Others are stories you might not have heard, but really should. All the stories are sourced from world folklore, but retold for modern ears. These are stories of wizards, knights, Vikings, dragons, princesses, and kings from the time when the world beyond the map was a dangerous and wonderful place.",
		# "episode_count": "40",
		# "avg_episode_duration": "20",
		# "link": "https://www.stitcher.com/podcast/jason-weiser/myths-and-legnen",
		# "similarity": "99",
		# "rating": "4.0",
		# "genres": ["Literature", "Fantasy"],
		# "similarities": [("Duration", "TBD"), ("No. Episodes", "TBD"), ("Genre", "TBD"), ("Description", "100")]},
		# {
		# "pic": "placeholder.jpg",
		# "name": "Coffee",
		# "description": "A podcast about coffee",
		# "episode_count": "100",
		# "avg_episode_duration": "15",
		# "link": "https://www.stitcher.com/podcast/studio71/coffee-talk-2",
		# "similarity": "5",
		# "rating": "1.5",
		# "genres": ["Food"],
		# "similarities": [("Duration", "15"), ("No. Episodes", "10"), ("Description", "0")]
		# }]

	# remove querried podcast from showing in result list, and round avg durration and episode count
	index_of_podcast = 0
	found_query = False
	for i in range(len(data_dict_list)):
		if(data_dict_list[i]['name'] == query):
			index_of_podcast = i
			found_query = True
		if(data_dict_list[i]["avg_episode_duration"] != "None"):
			data_dict_list[i]["avg_episode_duration"] = round(float(data_dict_list[i]["avg_episode_duration"]), 2)
		if(data_dict_list[i]["episode_count"] != "None"):
			data_dict_list[i]["episode_count"] = round(float(data_dict_list[i]["episode_count"]))
	if(found_query):
		data_dict_list.pop(index_of_podcast)

	return render_template('search.html', name=project_name, netid=net_id, data=data_dict_list, podcast_names=podcast_names, show_modal=True)
