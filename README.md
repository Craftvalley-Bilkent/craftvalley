This project uses Docker, so the first thing to do is to download Docker. For more information, please use the official documentation.

Similarly, you need to clone the project’s repository from GitHub to your system using “git clone”.

Then, using your operating system’s shell, navigate to the directory where you cloned the repository.

To run the project, execute the following commands in your operating system’s shell.
    docker build -t craftvalley .
    docker compose up -d
    
Once your terminal indicates that containers are up and functional, you can use Craftvalley at http://localhost:3000/auth/login/
    If the app is not working properly, go to the docker-containers, run the migration-1 container, and restart the web-1 container.
    
You can close the application from the terminal with the “docker compose down” command.
