# Audiencias Públicas
> Participate remotely in events via a three-paneled approach: live video, chat, and crowdsourced ranked questions. You can see the audiencias running in the following link <https://edemocracia.camara.leg.br/audiencias/>


## Installation for developers
 
### 1. Using Docker

Run the following command and all the necessary dependences will be installed and the project will start to run automatically:

```
 docker-compose up
```

Depending on how Docker/Docker Compose was installed in your machine you may need to run this command as a super user.

### 2. Installing Audiencias localy

#### Install dependences

First of all, you need to install [pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) and [npm](https://www.npmjs.com/get-npm). 

After install these dependencies enter inside the directory where you download this repository, and run the following commands in the root:
(P.S: You may need to run some of the following commands as super user)

```
pipenv install -r requirements.txt
apt install redis-server
npm install node-sass
```

After install redis check if it is running in your computer using:

```
systemctl status redis
```

If it is not, start it using:

```
systemctl enable redis
```

In case you need to restart it, it can be done with:

```
systemctl restart redis
```

#### Add Edem Navigation top bar

You just need to run the following commands if you are using it inside the e-Democracia. Otherwise you can skip then and go to the next section (Running the Audiencias).

Go to templates/components/edem-navigation directory

```
cd templates/components/edem-navigation
```

Run the following gits to get the git submodule of the edem navigation bar:

```
git submodule init
git submodule update --remote
```

This Edem Navigation will allow you to login into the audiencias with the e-Democracia login. In case you just want to run it see how it looks, you can login into the audiencias using an admin account. An admin user can be created using django admin commands.

#### Running the Audiencias

If you are inside and pipenv environment you can run it with:

```
pipenv run src/manage.py migrate
pipenv run src/manage.py runserver
```

Otherwise in case you are running it direct in your machine, inside the root of your directory, the following commands:

```
./manage.py migrate
./manage.py runserver
```

## Support

Fell free to create any issue on this repository and contact the team responsible to maintain this project here on GitHub ( @erivanio, @thiagonf, @joaopaulonsoares and @teogenesmoura) or via email: labhacker@camara.leg.br.

## Contributing
1. Fork of this repository
2. Write your code
3. Create a Pull Request
4. Our team will review your PR and merge as soon as possible!

## License
This project is under GPLv3 License

