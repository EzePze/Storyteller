# Storyteller

Storyteller is a token-based text generator that can take in either user input or use a random prompt from a text file the user has specified. The architecture is based on OpenAI's GPT-2 Transformer model, and includes models of varying complexities, listed as follows:

      1. 124M
      2. 355M
      3. 774M
      4. 1558M


The user is able to select any of these models and apply them to a writing style of their choice, e.g. the user could create a model that uses Shakespearean sonnets or the works of John Keats, and the models would generate text based on these writing styles, optionally with a custom prompt from the user. 

This software was created for my year 12 major work; many features and seemingly unnecessary inclusions in the package were required for my assignment. Regardless, this package will work for anyone, whether a developer curious in how GPT-2 works, or a consumer who just wants a friend to tell a story for them.

## Installation

Clone the repository or download it outright. After entering the new directory created for the package, you will need to install some dependencies using Python's 'pip' package installer. Enter the following into the command line:

    pip install -r requirements.txt

This will sequentially install all the required packages needed to run the software. After this, type

    python3 main.py

into the command line, and the software will initialise and prompt you with the following:

    It seems that you do not have the required models downloaded.
    These are required to generate text, and are, in total,
    approximately 10GB in size. Would you like to install them now? (y/n)

Input 'y' and press enter, and then the models will begin to download. After this, the software will be ready to use.

## Login Screen

The program will begin with a login screen, displaying the following:

       _________ __                       ___________    .__  .__
      /   _____//  |_  ___________ ___.__.\__    ___/___ |  | |  |   ___________
      \_____  \    __\/  _ \_  __ \   |  |  |    |_/ __ \|  | |  | _/ __ \_  __ \
      /        \|  | (  (_) |  | \/\___  |  |    |\  ___/|  |_|  |_\  ___/|  | \/
     /_______  /|__|  \____/|__|   /_____|  |____| \___  |____/____/\___  |__|
             \/                    \/                  \/               \/

    Welcome To StoryTeller.

    Do you wish to log in, or register a new user?

    [L]ogin
    [R]egister

All of the selection screens work by the format of [O]ption or [2] Option, where the key required to select the option is whatever is captured by the square brackets. For example, to select 'Option', the user would input an 'o' or 'O' in the first example, and a '2' in the second. 

The two options for the login screen are the following:

### Login

You will be taken to a login screen, where you will be asked to enter a username and password. If this is your first time, there will be no users, and you will be unable to login. If your login is successful, you will see

    Login successful. Welcome, (username)

and proceed to the Model Select screen. If it is not, you will revert back to the start screen above.

### Register

Under this choice, you will be prompted to enter a username and password which will be subsequently stored and encrypted. This will also generate a unique directory and text file which contains your unique models. i.e, user 'Ben' would have different models to user 'Jack'. These login details will be permanent, so don't forget your details.

## Model Select

This is the main hub of the software. In this screen, you will be prompted with the following:

    Select a model or create a new one:

    [0] New Model
    [1] Delete Model

And then your individual models will follow as options. Before we proceed onto the text generation, the 'New Model' and 'Delete Model' options are described below.

### New Model

Once on this screen, you will be prompted with

    Enter the name for your new model:

And, after you have entered a name,

    Enter the name of the text file to be used for modelling (needs to be in the /Storyteller folder):

Assuming that the model does not already exist and that the text file you have inputted exists, the model will be created and you can immediately begin using it straight after it is created. After using this function, you will be returned to the Model Select screen with your options updated to accomodate the new model.

### Delete Model

On this screen, you will be shown a list of the available models that you can delete. These will be unique to your model list. An example list is as follows:

    [0] Shakespeare
    [1] Nietzsche
    [2] Sun Tzu
    [3] J.K. Rowling

If the user entered '2', they would be taken to a confirmation screen:

    Are you sure you wish to delete model 'Sun Tzu'? (y/n)

And after they entered 'y', the 'Sun Tzu' model would be deleted and the user would be taken back to the Model Select screen.

## Text Generation

After selecting an existing model as an option, the user will be taken to a series of configuration screens. Firstly, they will be asked whether they wish to use a custom prompt or a prompt from the text file they used in the creation of the model:

    Select a mode:

    [C]ustom prompt
    [T]ext file prompt

After the user has chosen an option, they will proceed to the complexity selection screen, in which they will be provided with four configuration options for the complexity and speed of the model:

    Choose the level of complexity for the model:

    [0] Speed [----------] Quality [--        ]
    [1] Speed [-------   ] Quality [----      ]
    [2] Speed [----      ] Quality [-------   ]
    [3] Speed [--        ] Quality [----------]

**[WARNING: THE HIGHEST QUALITY MODEL REQUIRES AT LEAST 16GB OF RAM TO USE EFFECTIVELY. IF YOUR COMPUTER DOES NOT HAVE 16GB OF RAM, THE MODEL MAY GET STUCK INDEFINITELY AND NEVER GENERATE TEXT, DESPITE THE PROGRAM RUNNING OPTIMALLY]**

After the user has chosen a complexity, they will be either shown the prompt that will be used to generate text, or they will prompted for a custom input, depending upon whether they chose to use a custom prompt or not.

    Model prompt >>> I think The Beatles had an underwhelming first album, but

    Generating text with the prompt "I think The Beatles had an underwhelming first album, but "

After this, the model will generate the text. This can take between 1-10 minutes, depending on the level of complexity chosen. Once generated, the text will be displayed. After this, the user will be taken back to the Model Select screen, where they can generate text with a different model, create a new model, or delete an existing one. This entire process will repeat until the user quits using Ctrl-C, which can be used at anytime to quit.

## Full Examples

### Custom Prompt Text Generation

For this example, the prompt "To be or not to be, that is the question:" was used with a model based on various Shakespearean sonnets to generate custom text:

    Select a model or create a new one:

    [0] New Model
    [1] Delete Model
    [2] General
    [3] Nietzsche
    [4] Shakespeare

    4

    Select a mode:

    [C]ustom prompt
    [T]ext file prompt

    c

    Choose the level of complexity for the model:

    [0] Speed [----------] Quality [--        ]
    [1] Speed [-------   ] Quality [----      ]
    [2] Speed [----      ] Quality [-------   ]
    [3] Speed [--        ] Quality [----------]

    2

    Model prompt >>> To be or not to be, that is the question:
    Generating text with prompt:

    "To be or not to be, that is the question:"

    ================================================================================
    I indeed shall know part here, part where there is to be lost, Of thy love, no more than if with thee Jove had his
    question; And when I can have thee there again, I shall think to blush. XXXII Thou lover, near me shall the gods stand,
    How much my own wishes seem to stretch Those carvings of the coffers of Fate; From another world I bid to see thee, In the
    Moment is thy wont amid rest: Reach me, and I will tell thee all. XXXIII Lest thy hopes of a friend-market Wrong me, stand
    at thy deed, And e'en afterward relax at rest; (Of thy late deeds I never understood; But a thousand or near ten thousand
    mistakes have I made, When Willian was father of the reins.) XXXIV Then must I be glad I sent thee away Which in truth I
    never could have your wish. If thou art with me still O generation's heir, Come back now. XXXV Or I am long standing here,
    however many once I show, And now far from fate be pacing in hall, And o'er what paths doth wander; For now ere I
    dauntless am I, on what I after might shake, And with quick eyes know the raging waves Suspend bowels as chiefly high.
    XXXVI To change may I not fail fittest for thee-- But if now I come to bath you and lie by you, And lay hold upon a rule
    with which I've cared-- Other well I know this think I well answer, hating and in love. XXXVII Alas thou right same--
    ruined art thou! Thy girl seized without fair chance To bind upon Love's favourite lap; But have I given thee return that
    what's now borrowed, With clubgrip and all its chain, Had issues by break of day. XXXVIII Thy birth pleasing I had dull so
    the Weary; But now my time is near-done-- Death's happy day The thing I must be happy my happiness. XXXIX Weep, wretched
    couple-- Time may not heal 't device, Then sweet honeyed heart is quaff'd from brier brush-- XXXX Rose blind in
    susceptible heart, new trial wearing black glimmer Or more happiness is wrapped up in darker slumber; Burnish thy damn'd
    senses-- Who blurts what?-- whether I see or hear Your answer-- thou, o Romeo. XXXXI Then say, I cannot call thee ever
    after, That one hour we had half a day
    ================================================================================

### Creating and Deleting Models

For this example, a model named 'shakespeareCopy' will be created that uses the 'shakespeare.txt' data file, and will be subsequently deleted.

    Select a model or create a new one:

    [0] New Model
    [1] Delete Model
    [2] General
    [3] Nietzsche
    [4] Shakespeare

    0


    Enter the name for your new model: shakespeareCopy

    Enter the name of the text file to be used for modelling (needs to be in the /Storyteller folder): shakespeare.txt

    Created model 'shakespearecopy'

    Select a model or create a new one:

    [0] New Model
    [1] Delete Model
    [2] General
    [3] Nietzsche
    [4] Shakespeare
    [5] Shakespearecopy

    1


    Which model do you wish to delete?

    [0] General
    [1] Nietzsche
    [2] Shakespeare
    [3] Shakespearecopy

    3
    Are you sure you wish to delete model 'shakespearecopy'? (y/n)

    y

    Deleted model 'shakespearecopy'


    Returning to model selection screen...


    Select a model or create a new one:

    [0] New Model
    [1] Delete Model
    [2] General
    [3] Nietzsche
    [4] Shakespeare

### Generating Text From Text File Input

In this last example, text will be generated using a random sample from a model that was based on an essay by Friedrich Nietzsche:

    Select a model or create a new one:

    [0] New Model
    [1] Delete Model
    [2] General
    [3] Nietzsche
    [4] Shakespeare

    3

    Select a mode:

    [C]ustom prompt
    [T]ext file prompt

    t

    Choose the level of complexity for the model:

    [0] Speed [----------] Quality [--        ]
    [1] Speed [-------   ] Quality [----      ]
    [2] Speed [----      ] Quality [-------   ]
    [3] Speed [--        ] Quality [----------]

    2
    Generating text with prompt:

     "the expense of all serious things! Gods are fond of ridicule: it seems that they cannot refrain from laughter even in
     holy matters. 295. The genius of the heart, as that great mysterious one possesses it, the tempter-god and born rat-
     catcher of consciences, whose voice can descend into the nether-world of every soul, who neither speaks a word nor casts
     a glance in which there may not be some motive or touch of allurement, to whose perfection it pertains that he knows how
     to appear,--not as he is, but in a guise which acts as an ADDITIONAL constraint on his followers to press ever closer to
     him, to follow him more cordially and thoroughly;--the genius of the heart, which imposes silence and attention on
     everything loud and self-conceited, which smoothes rough souls and makes them taste a new longing--to lie placid as a
     mirror, that the deep heavens may be reflected in them;--the genius of the heart, which teaches the clumsy and too hasty
     hand to hesitate, and to grasp more delicately; which scents the hidden and forgotten treasure, the drop of goodness and
     sweet spirituality under thick dark ice, and is a divining-rod for every grain of gold, long"



    ================================================================================
     ago extracted from theÿthen cold and waning soil which, a long time before him, had been baptized in this ?the culpritile
     contagion, through which the offspring of kingly litter must have come into every tribe and country. But


    79


    you see an example of this genius. The emperor, just after he had forthwith put an end to all perplexities by conviction
    that the first person to unveil Monotheism was Zeno, whom he believed he in cycles produced; the clergy, after the common
    experience of nations who believed in every Bible and every proportion, after the fatal end caused by the scattered
    populations of the nations--after all these things, these sublime tests, these infallible earthly guarantees to truth,
    people had cultivated the fine and homiletical acæsthetics: the yeah kingdom, preaching the

    cryms of Christ, and training scribes to blush to reflect life in the working, panting believers; a people, who felt
    depressed to education and encouraged poverty; a people led to the crucifixion by the candidate, emulated by kings and
    emperors; a people, who and who-observant preached every day, and them as all august institutions celebrated the grieving
    Mother turn disturbed by Utterance; a people, not ignorant of philosopher and other epithets, ready to want remedies, to
    desire penances, to forgo remonstrances, or to allow every human act to exist without arousing discontent and hatred-- the
    genius of the heart, applied to every way of existence, deserving still more sharp observation away from kings, all
    factions, Protestants, Jews, and parties, and misdeeds by omission or execution: the genius of the heart, that had
    incredible efforts to inflict from among his cruel pigs the curse of vermin seed, which burns thought like an infernal
    fire. But have you not already traced with etymological drawings that same monstrous fiend to the fabulous literary
    creation which this pastor calls Theureus, who restores myth by deception the greatness of needs and the stagnant liberty
    of imagination in men to the full: Timid in philosophy, and even more so in something which was neither there nor there,
    as applied to solids and liquids. You attribute Theiberius Venus to the old philosophers and checkmans facial ioisperson
    with the notes of puns and fasces. For if the homiletical satisfaction of Theophile Venus, different from all others--in
    which the thigh, a relation, and place do not enter into
    ================================================================================
