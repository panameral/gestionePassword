mkdir ~/.gestionePassword
cp ./* ~/.gestionePassword
echo 'current_folder=$(pwd) 
cd ~ 
python ~/.gestionePassword/Main.py 
cd $pwd' > pypass
mv pypass /bin/pypass
