mkdir ~/.gestionePassword
cp ./* ~/.gestionePassword
echo 'current_folder=$(pwd) 
cd ~/.gestionePassword/Main.py 
python ./Main.py 
cd $pwd' > pypass
mv pypass /bin/pypass
