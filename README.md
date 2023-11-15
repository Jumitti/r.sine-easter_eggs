# r.sine Easter Eggs Finder
<img style = "width: 100%; height: 100%;" src="https://r.sine.com/wellplayed" alt=""/>

## Description
[r.sine](https://r.sine.com/index) is a website that displays a random image or gif each time the page is refreshed. 
The site can be accessed at https://r.sine.com/index. However, while poking around, 
I realized that if you replace "index" with other words, the images are no longer random. We have 3 possible cases. 
Either the word displays random images (e.g. https://r.sine.com/index ), or the word displays a single image 
(e.g. https://r.sine.com/admin), or the word displays a "buffer" image which is used for several words, 
probably when the word is not addressed to an image. I decided to use a script to discover all the possible words to use.
Yes, it's stupid. Welcome to the internet.

<img style = "width: 100%; height: 100%;" src="https://r.sine.com/www" alt=""/>

## How it works

So it's a pretty straightforward process. We know that "index" offers random images (**Cond1**), 
that some words link to the same photo (**Cond2**) and that some words are only affiliated with a single image (**Cond3**).

- **Cond1**: random image → ```random_pictures.txt```
- **Cond2**: buffer image used for several words → ```same_pictures.txt```
- **Cond3**: single image for one word → ```unique_pictures.txt``` | single image for 2 or more words → ```unique_pictures_2words.txt```

So basically, we make requests for each word in the dictionary !
For this, I use either [Wikipedia's word frequency lists](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/PG/2006/04/1-10000) 
or ```words_dictionary.json``` from [english-words](https://github.com/dwyl/english-words).

Then I make a first request for a specific word and retrieve the image source code. 
I make a second request with the same word. If the 2 source codes are not similar, 
then we're in the case of the word "index" for example, where we'll only have random images (**Cond1**). 
If the 2 source codes are similar, this means that the image is necessarily identical and that the word leads 
to a specific image. 
Then, if the 2 source codes are identical, I check whether the latter is similar to a source code already known for 
the other words already screened. If it's identical, then the word leads to the "buffer" image (**Cond2**). 
If not, the word leads to a unique image (**Cond3**).

After that, I made the script to limit the number of requests, but that's a technicality that no one cares about.

## Sorted words and examples

Lists are in ```output``` folder

- **Cond1**: random image → ```random_pictures.txt``` (e.g. https://r.sine.com/index for legal reasons, I don't display random images)


- **Cond2**: buffer image used for several words → ```same_pictures.txt``` (e.g. https://r.sine.com/nicetry)
I don't know why this one don't works to display the image <img style = "width: 100%; height: 100%;" src="https://r.sine.com/nicetry"/>


- **Cond3**: 
  - single image for one word → ```unique_pictures.txt``` (e.g. https://r.sine.com/admin)
    <img style = "width: 100%; height: 100%;" src="https://r.sine.com/admin"/>
  - single image for 2 or more words → ```unique_pictures_2words.txt``` (e.g. https://r.sine.com/bird and https://r.sine.com/parrot)
  
    | https://r.sine.com/bird                                                   | https://r.sine.com/parrot                                                   |
    |---------------------------------------------------------------------------|-----------------------------------------------------------------------------|
    | <img style = "width: 100%; height: 100%;" src="https://r.sine.com/bird"/> | <img style = "width: 100%; height: 100%;" src="https://r.sine.com/parrot"/> |
  

## Special words

In the ```special_words``` folder, you will find all the words leading to unique outputs (**Cond3**) but which are not images.

Some words are internet pages. They are no longer executable on r.sine.com but you can open them by downloading the html and opening them with a browser.

### ```chicken```

A scientific chicken article in PDF format. Thank you r.sine.com 😅

### ```content``` ```farmer```

Music group promotion web pages ?

### ```drinking```

It's a comic strip on a white background. The white background and the way the GIF is generated is quite atypical.

### ```heaven```

Web page to comment anonymously on photos of Rachel Sterne Twitter ?

### ```lamppost``` ```ready``` ```smart```

Images that no longer work on r.sine.com. HTML work.

### ```monitors``` ```robots```

A mystery... I have no idea about it

### ```r```

I don't know if it's a bug or if it's intentional. It's a piece of code that helps us understand how images are returned to us on https://r.sine.com/index.

### ```topmen```

Leads to https://www.youtube.com/watch?v=yoy4_h7Pb3M (html broken)

## Disclaimer

The images on r.sine.com may offend the sensibilities of users. If you do not have the majority (of your country), 
I disclaim all responsibility for what you find on this site. This GitHub project is just a curiosity about another 
Internet curiosity.
