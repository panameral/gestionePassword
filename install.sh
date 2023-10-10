mkdir ~/.gestionePassword
cp ./* ~/.gestionePassword
echo 'current_folder=$(pwd) 
cd ~ 
python ~/.gestionePassword/Main.py 
cd ~/.gestionePassword/Main.py 
python ./Main.py 
cd $pwd' > pypass
sudo mv pypass /bin/pypass
