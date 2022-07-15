# Genre based story generator

![webpage_intro](https://github.com/aditya2029/genre-storygenerator/blob/main/app/static/img/front_page.jpg)
![project_description](https://github.com/aditya2029/genre-storygenerator/blob/main/app/static/img/description_proj.jpg)
![genre](https://github.com/aditya2029/genre-storygenerator/blob/main/app/static/img/genre_page.jpg)

### Introduction:

In this project, we are generating short stories (100 words) based on the given six genre (drama, thriller, action, superhero, scifi and horror) by fine-tuning GPT-Neo model.
This model is deployed on cocalc server using flask.

### Dataset:

The dataset is taken from:
[six_genre_dataset](https://drive.google.com/file/d/11FgexOt7PWxFnn9TbkMaEYVEo7gkHwkl/view)
which is the created by Pranav Varedu by combining [Wikipedia movie plots](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots) and scrapping superhero comics data from Wikipedia.

This dataset contains over 30,000 stories.

### Approach:

For generating the stories, I have fine-tuned the GPT-Neo model which is comparable to GPT-3 but of small size using given dataset.
I have trained six seperate model for different genres. User will give input (genre and prompt) from the website and the story will be generated based on that.

### Files and Directories:

The architecture of files and directories are as follows:

* app/
	* model/
		* model_url
	*	static/
		*	css/
		*	img/
		* js/
		* favicon.ico	
	*	templates/
		*	Write-your-story-with-AI.html
		*	writer_home.html
	*	main.py
	*	requirements.txt
	*	utils.py
* code_files/
	* data_preprocessing.ipynb
	* model_text_generation.ipynb
	* training_genre_models.ipynb
* .gitignore
* Dockerfile
* Readme.md
* config.py
* entrypoint.sh
* host_config
* nginx_host

#### Model:

In the model folder, the URL [model weights and config files](https://drive.google.com/drive/folders/1XeHl9RHsJ7HSgfsSGBC1nsfk_Lavk18v?usp=sharing) is given from which you can download the respective files based on the genre. The file directory after this process should look like this:

* app/
	* model/
		* drama_files/
			* pytorch_model.bin
			* config.json
		* horror_files/
			* pytorch_model.bin
			* config.json
		* thriller_files/
			* pytorch_model.bin
			* config.json
		* superhero_files/
			* pytorch_model.bin
			* config.json
		* scifi_files/
			* pytorch_model.bin
			* config.json
		* action_files/
			* pytorch_model.bin
			* config.json

#### Static:

This folder will give you the independency to change HTML templates according to your usecase.

### Running the application:

Make sure to install the dependencies of the following:

* Flask
* aitextgen
* pytorch

Also install the packages given is **requirements.txt** file.

Then clone the repository:

git clone https://github.com/aditya2029/genre-storygenerator

Run the web application by:

python3 -m main

### Acknowledgement:

This project is a part of NLP Crash Crouse by AI Camp (https://www.ai-camp.org/)
# -SC22-BatchB-wireless-union
