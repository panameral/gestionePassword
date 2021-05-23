mkdir ~/.gestionePassword
cp ./* ~/.gestionePassword
echo 'current_folder=$(pwd) 
<<<<<<< HEAD
cd ~ 
python ~/.gestionePassword/Main.py 
=======
cd ~/.gestionePassword/Main.py 
python ./Main.py 
>>>>>>> 531bd17359e56783fc16f82e055a4d9191493fbe
cd $pwd' > pypass
mv pypass /bin/pypass
