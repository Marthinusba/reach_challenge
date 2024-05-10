## DataOps Engineer Challenge

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--

[![LinkedIn][linkedin-shield]][linkedin-url]




<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The project ingests daily Covid-19 related data made available by the API described [here][https://covidtracking.com/data/api/version-2].
The projects performas extraction, transfoarmation and loading processes on the data returned from the api. The data is returned as a JSON object and 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][python]][python-url]
* [![React][React.js]][React-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Certain assumptions are made with the deploying of the projects, such as experience with git and linux commands and having git and docker installed.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* git
* docker

### Installation

Steps to install and run program

1. Clone the repo
   ```sh
   git clone https://github.com/Marthinusba/reach_challenge.git
   ```
2. Change directory to reach-challenge
   ```sh
   cd reach-challenge
   ```
3. Run docker compose command
   ```sh
   docker-compose up --build
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. To access the Postgres database in docker to perform analysis.
    ```sh
    docker exec -it docker_postgresql bash
    ```
2. And to access the database:
    ```sh
    psql -h docker_postgresql -d postgres_db -U postgres_user
    ```
3. The password required is ```postgres_password```

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/marthinusbasson/

[python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[python-url]: https://python.org/
