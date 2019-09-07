# 292 Pasir Panjang Road App Store

This is a big project. The main purpose for this project is for us to quickly develop and deploy interesting applications.

## The work flow

1. Generate templates for `sub projects`, which can be built using __Docker__. The information for each of the project will be stored in `config/config.yml`. Each sub project will be assigned a unique port number.
2. With __TravisCI__, we can automate the build process for each of the sub projects and push the docker images onto docker hub.
3. If the application requires deployment (specified in `config/config.yml`), then __TravisCI__ will ask server to pull the latest version of the app image and run the app on server.

## To get started

1. clone the repo via

```bash
git clone https://github.com/292-pasir-panjang-road/app-store.git
```

2. set up python environment management tool (Optional)

```bash
brew update && brew install pipenv
cd project/root
pipenv --python 3
pipenv shell
```

3. install requirements

```bash
pip install -r requirements.txt
```

4. create your app

```bash
python register_app.py --name $app_name --author $author --subdomain $sub_domain ...
```

Till here, you should be able to see your app config inside `config/config.yml` and see your app files under `sub_projects/$sub_domain`

5. develop you application

For now, we only provide simple __Flask__ application template. Feel free to add some ;)
After development, make sure to change your Dockerfile and `start.sh` accordingly.

6. build & deploy your app

If you want to run your app on the server, please modify `config/config.yml` and put _deploy_ to be _true_. Then, as soon as you push your code, the docker image will run on the server.
To verify it, you can ssh onto the server as user `292ppr` and run to check whether the image is pulled and whether the container is running

```bash
sudo docker images
sudo docker ps
```

