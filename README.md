# HelloWorld2025
## Inspiration
Oftentimes, the only movies people know about are the ones with high advertising budgets, and streaming services recommend movies based on what profits them the most, not what is most enjoyable for YOU to watch. Meanwhile, AI chatbots usually recommend picks that are popular online. So, we developed a program to recommend movies using our unique rating method, helping you find the best movies that suit your tastes.
## What it does
Movie Recommender is a personalized recommender engine that:
- Takes your favorite movies and turns your personal ratings into data 
- Converts this data into a vector in 11 dimensions
- Turns TMDB API data into an 11-D vector space
- Finds and recommends movie vectors near your movie vector

## How we built it
### General Process
The Movie Recommender's front-end is primarily built with Streamlit and hosted by its cloud service—but the process begins long before this. The first step was deciding where to find movie data. Thankfully, we quickly found The Movie Database (TMDB), and were able to use the API to retrieve movie data in JSON format and convert it to CSV format. Next, we needed a unique way to make the movie data workable. Our solution was vectors:
> We need a method, or a consistent way of converting movie data into a k-dimensional vector. Honestly, it shouldn't be too hard, where we take the rating value and some genre values as components. For example:
>
>     # Generic
>     movie_name = [rating, happy, sad, scary]
>     # Specific
>     the_shining = [8.4, 0.0, 6.0, 9.0]
>
> The rating value can be the movie. We can get genre values by weighing genre tags: it has 3 horror tags, where each horror tag contributes 2 to the sad value, and 3 to the scare value. This is how we can convert the API data to our own personal data.

This quote is from the initial proposal for the project, and carries the theme for the rest of the project.
After we decided on a solid metric to convert genre tags into genre values, we needed a way to organize the vector data into a searchable tree to find nearby vectors. Thankfully, we discovered the k-d tree, the perfect data structure for our needs. 
> We can use a distance-relevance data structure since we are using vectors as data points. I was thinking of a k-d tree (k-dimensional tree) because it suits our needs exactly. Essentially, turning our data into a K-d tree converts our data to a usable data structure in a timely fashion, while maintaining its usability for later use.

Once we generated a k-d tree for our 11-D vectors, we focused on user input. On the front-end, users select the genres they want to explore and rate at least two movies they’ve seen. Using an advanced algorithm, we consolidate multiple user ratings into a single fictitious movie vector. From there, a nearest-neighbor search identifies the “n” closest vectors in the k-d tree. The result: personalized movie recommendations tailored both to your ratings and the genres you want. Finally, the front-end brings everything together in a clean, intuitive interface.
### Distribution of Tasks
- Front-end: One developer designed and implemented the Streamlit UI, handled all user inputs, integrated the recommendation engine within the interface, and styled several application elements with HTML/CSS for a polished user experience.
- Data & API: Two developers managed the TMDB API, CSV processing, vector conversions, and scoring mechanism that transformed qualitative data into quantitative vectors.
- Algorithms: One developer focused on k-d tree generation and nearest-neighbor search, creating a reusable method for querying recommendations.

Each sub-team worked modularly so components remained functionally independent but easy to integrate, resulting in a polished, functional final product. Once coding was complete, we collaborated on documentation and presentation to showcase the project.
## Challenges we ran into
We had many technical challenges:
- Converting a pandas series to the correct datatype
- Pandas filtering
- CSV formatting
- UI permissions with Streamlit
- Streamlit wheel with numpy created from scratch
- Creating a fictitious movie vector

## Accomplishments that we're proud of
We’re proud of everything. As a near-completely inexperienced team, this was our first large-scale collaborative project, and we succeeded in building a fully functional, polished product. Beyond coding, we leveraged strong intrapersonal communication and teamwork, ensuring every module fit seamlessly into the final project. This experience was a major success for all of us.
## What we learned
When we divided tasks up, we considered each team member's strengths and weaknesses based on programming experience. For example, some people had experience in data, algorithms, or front-end development. By realizing where we could most efficiently devote roles, each member could expand their pre-existing knowledge and go beyond their comfort zone to ship an incredible product. 
For example, our data team learned tons of debugging and management strategies for working with CSVs, our algorithm team learned about two new structures, and our front-end team implemented new techniques.
## What's next for Movie Recommender
We have many plans for the future of Movie Recommender:
- Refine the genre scoring method using data analysis and further testing
- Change vector scaling to give importance to certain values over others
- Re-work the way we use user input to deal with outliers in data
- Alternatively, re-work to circle inputs into batches and make multiple fictitious movie vectors
- Add more movies to the recommender/ask how many you want
- So much more
## Resources
Links: [Devpost Link](https://devpost.com/software/movie-recommender-y1i3zc), [Streamlit Link](https://hw25movierecommender.streamlit.app/)
