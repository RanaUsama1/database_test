
<h1> Vulgaris Platform </h1>

![JavaScript](https://img.shields.io/badge/javascript-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black)
![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![NPM](https://img.shields.io/badge/NPM-%23CB3837.svg?style=for-the-badge&logo=npm&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

[Università La Sapienza Roma](https://www.uniroma1.it/en), [Dipartimento di Informatica](https://www.studiareinformatica.uniroma1.it/)

![Sapienza Università di Roma](/logos/sapienza-big.png)

### Credits

[`federico-rosatelli`](https://github.com/federico-rosatelli) [`Mat`](https://github.com/AxnNxs) [`Loriv3`](https://github.com/Loriv3) [`Samsey`](https://github.com/Samseys) [`Calli`](https://github.com/BboyCaligola)


### MicroAlgaeDB
This repository is part of MicroAlgae DB project, formed by various modules. Visit the homepage at link https://github.com/BITSapienza for a general guide and automatic installation through docker-compose.


# Vulgaris Platform Description
Front-end for views and tables in web interface, coded in VueJS 

# Home of Vuglaris Platform
![](/logos/Homepage.png)

# Vue Views
The views present in the web application are:
- `HomeView`:  The Home view is responsible for fetching and rendering dynamic markdown content, for display.

- `TaxonomyView`: The Taxonomy view displays hierarchical taxonomy information, including scientific names and ranks, allowing users to navigate through the taxonomy tree and access detailed information for each taxon.

- `SearchTableView`: The Taxon Search view allows users to search for taxonomy information based on scientific names or taxon IDs. It provides filters for products and locations, and displays search results in a table format with relevant details such as the number of nucleotides, proteins, and genomes associated with each taxon.

<img src="logos/SearchView.png" width="800" height="500">

- `OrganismView`:  This Vue code represents a component for displaying organism information, including proteins or nucleotides, with the ability to view detailed data and copy names to the clipboard.

- `SRAView`: This Vue code represents a component for displaying genomic information, including the scientific name and the number of associated bio projects. It allows users to view detailed information about a specific genome and if present, the analysis.

# Vue Components
Vue components coded for the project are:

- `BioProjComp`: This Vue component renders a hierarchical list of BioProjects, BioSamples, Experiments, and Runs. It displays information such as IDs and the number of associated items. It also includes a section containing the Volcano and Heat plots if the analysis was done.

- `NucleotideComp`: This Vue component displays information related to a genetic sequence. It shows the source, locus, and comments of the sequence. It also display each feature key and its associated qualifiers. The component, if present, displays the qualifier name and value, and provides a link for the "product" qualifier.

# How To Run The Platform

To run the Vulgaris Platform you need to install all Javascript dependencies from `package.json` file.
To do so you can run:
```shell
npm install
```
After installing the dependencies you can start the application via npm doing:
```shell
npm run dev
```
Vite will create a real time web-application in `http://localhost:5173/`. <br />
To install and run the application in production mode just run:
```shell
npm run build-prod
```

