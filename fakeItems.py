#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from textwrap import dedent
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import (
    Base, Item, Category, User, References,
    user_with_item, category_with_item, DB_CONN_URI
)


engine = create_engine(DB_CONN_URI)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Add User Cielo
user = User(email='cielosplayground@gmail.com',
            username='cielo',
            password='password')

session.add(user)
session.commit()


# Category for Animation and Manga
anime = Category(name='Animation')

session.add(anime)
session.commit()

uwi1 = user_with_item()
refer1 = References(rlink="https://en.wikipedia.org/wiki/Your_Name")
anime1 = Item(name='君の名は(Your Name)',
              description=dedent("""\
              High school girl Mitsuha lives in the town of Itomori in Japan's
              mountainous Hida region. Bored, she wishes to be a handsome boy
              in her next life. She begins switching bodies intermittently
              with Taki, a high school boy in Tokyo, when they wake up. They
              communicate by leaving notes in Mitsuha's notebook and memos on
              Taki's phone, and sometimes by writing on each other's skin.
              Mitsuha causes Taki to develop a relationship with his coworker
              Miki, while Taki causes Mitsuha to become popular in school.

              Taki, as Mitsuha, accompanies her grandmother and sister to
              leave the ritual alcohol kuchikamizake, made by Mitsuha, as an
              offering at the shrine on a mountaintop outside the town. The
              shrine is believed to represent the body of the village guardian
              god who rules human experiences and connections. Mitsuha's
              latest note tells Taki about a comet expected to pass Earth on
              the day of her town festival.

              One day, Taki wakes up in his body. After an unsuccessful date
              with Miki, he tries to call Mitsuha, but cannot reach her, and
              the body switching ends. He decides to visit Itomori, but does
              not know its name, his memories of it are fading, and Mitsuha's
              messages have disappeared. A restaurant owner in Hida finally
              recognizes Itomori from Taki's sketch and tells him it was
              destroyed by a fragment of the comet. Taki finds Mitsuha's name
              in the records of fatalities and discovers the date of the
              disaster. He realizes their timelines were separated by three
              years.

              Taki goes to the shrine to drink Mitsuha's kuchikamizake, hoping
              to reconnect with her body and warn her of the comet strike.
              Through a vision, Taki discovers that Mitsuha, having fallen in
              love with him, met his past self while trying to meet him
              personally. He wakes in her body on the morning of the town
              festival; Mitsuha's grandmother deduces his identity, and tells
              him the body switching is part of the Miyamizu family history as
              caretakers of the shrine. He convinces Mitsuha's friends Tessie
              and Sayaka to help evacuate the town by cutting the power and
              broadcasting a false emergency alert, but the plan fails. He
              realizes that Mitsuha must be in his body at the shrine and goes
              back to find her.

              Mitsuha wakes up in Taki's body at the shrine. Although they
              sense each other's presence, they are separated by three years.
              However, when twilight falls, they return to their own bodies
              and meet. They attempt to write each other's names on their
              hands so they will remember each other, but twilight passes and
              Mitsuha disappears before she can write hers.

              As Mitsuha races back to town to convince her estranged father,
              the Itomori mayor, to evacuate the town, her memories of Taki
              start to fade. She realizes that Taki wrote "I love you" on her
              hand instead of his name. The comet piece crashes to Earth,
              destroying Itomori. Taki wakes up in his own time at the shrine,
              remembering nothing.

              Five years later, Taki has graduated from university and is
              searching for a job. He senses he is missing something important,
              and learns that inhabitants of Itomori survived by following the
              mayor's order. He recognizes Tessie and Sayaka in a Tokyo
              restaurant, now engaged, but cannot identify them, and both Taki
              and Mitsuha's friends and family are shown to be pursuing their
              own paths. One day, Taki and Mitsuha see each other when their
              trains draw parallel, and are compelled to disembark and search
              for one another, finally meeting on a staircase. Feeling they
              have met before, they simultaneously ask for each other's name.
              """),
              refers=[refer1],
              imageURI="images/Kimi_No_Namae_Wa.png",
              lastEditTime=datetime.now())
uwi1.item = anime1
user.items.append(uwi1)
anime.items.append(anime1)

session.commit()

uwi2 = user_with_item()
refer2 = References(rlink="https://en.wikipedia.org/wiki/Anohana"
                    ":_The_Flower_We_Saw_That_Day")
anime2 = Item(name='あの日見た花の名前を僕達はまだ知らない(AnoHana)',
              description="It is revealed that all of the group members "
              "blame themselves for Menma's death and long-hidden feelings "
              "are rekindled. The group struggles as they grow from trying to "
              "Menma move on and help each other move on as well.",
              refers=[refer2],
              imageURI="images/AnoHana.jpg",
              lastEditTime=datetime.now())
uwi2.item = anime2
user.items.append(uwi2)
anime.items.append(anime2)

session.commit()

uwi3 = user_with_item()
refer3 = References(rlink="https://en.wikipedia.org/wiki/Your_Lie_in_April")
anime3 = Item(name="四月は君の嘘(Your Lie in April)",
              description="Much to everyone's sadness, Kaori dies due to the "
              "surgery, but leaves a letter to Kōsei which is given to him by "
              "her parents at her funeral in which she eventually states that "
              "she was in love with Kōsei the whole time, and she lied that "
              "she had a crush on Watari to get closer to him while not "
              "hurting Tsubaki's (who also has a crush on Kōsei) feelings. "
              "This was her lie: a lie she told in April.",
              refers=[refer3],
              imageURI="images/Your_Lie_In_April.jpg",
              lastEditTime=datetime.now())

uwi3.item = anime3
user.items.append(uwi3)
anime.items.append(anime3)

session.commit()

uwi4 = user_with_item()
refer4 = References(rlink="https://en.wikipedia.org/wiki/Hanasaku_Iroha")
anime4 = Item(name="花咲くいろは(The Blooming Colors)",
              description="Initially feeling discouraged, she decides to use "
              "her circumstances as an opportunity to change herself for the "
              "better and to make amends with her deteriorating relationship "
              "with the Kissuisō's staff for a more prominent future.",
              refers=[refer4],
              imageURI="images/The_Blooming_Colors.jpg",
              lastEditTime=datetime.now())
uwi4.item = anime4
user.items.append(uwi4)
anime.items.append(anime4)

session.commit()

uwi5 = user_with_item()
refer5 = References(rlink="https://en.wikipedia.org/wiki/"
                    "A_Certain_Scientific_Railgun")
anime5 = Item(name="とある科学の超電磁砲 レールガン(A Certain Scientific Railgun)",
              description="In the futuristic Academy City, which is made up "
              "of 80% students, many of whom are espers possessing unique "
              "psychic powers, Mikoto Misaka is an electromaster who is the "
              "third strongest of a mere seven espers who have been given the "
              "rank of Level 5. The series focuses on the exploits of Mikoto "
              "and her friends; Kuroko Shirai, Kazari Uiharu, and Ruiko Saten "
              ", prior to and during the events of A Certain Magical Index.",
              refers=[refer5],
              imageURI="images/A_Certain_Scientific_Railgun.jpg",
              lastEditTime=datetime.now())
uwi5.item = anime5
user.items.append(uwi5)
anime.items.append(anime5)

session.commit()

uwi6 = user_with_item()
refer6 = References(rlink="https://en.wikipedia.org/wiki/Hyouka")
anime6 = Item(name="氷菓(Hyouka)",
              description="At the request of his older sister, student Hotaro "
              "Oreki joins Kamiyama High School's Classic Literature Club to "
              "stop it from being abolished, joined by fellow members Eru "
              "Chitanda, Satoshi Fukube and Mayaka Ibara. The story is set in "
              "Kamiyama City, a fictional city in Gifu Prefecture that the "
              "author based on his real hometown of Takayama, also in Gifu. "
              "The fictional Kamiyama High School is based upon the real life "
              "Hida High School. They begin to solve various mysteries, both "
              "to help with their club and at Eru's requests.",
              refers=[refer6],
              lastEditTime=datetime.now())
uwi6.item = anime6
user.items.append(uwi6)
anime.items.append(anime6)

session.commit()


# Category Detectives
detective = Category(name="Mysterious & Detectives")

detective.items.append(anime6)
session.commit()

uwi7 = user_with_item()
refer7 = References(rlink="https://en.wikipedia.org/wiki/The_A.B.C._Murders")
detective1 = Item(name="The A.B.C. Murders",
                  description="Returning from South America, Arthur Hastings "
                  "meets with his old friend Hercule Poirot, at his new flat "
                  "in London. Poirot shows him a mysterious letter he "
                  "received signed 'A.B.C.', that details a crime that is to "
                  "committed very soon in August, which he suspects will be a "
                  "murder. Two more letters of the same nature soon arrive to "
                  "his flat, each prior to a murder being carried out by "
                  "A.B.C., and done in alphabetical order: Alice Ascher, "
                  "killed in her tobacco shop in Andover; Elizabeth 'Betty' "
                  "Barnard, a flirty waitress killed on the beach at Bexhill; "
                  "and Sir Carmichael Clarke, a wealthy man killed at his "
                  "home in Churston. In each murder, an ABC railway guide is "
                  "left beside the victim.",
                  refers=[refer7],
                  lastEditTime=datetime.now(),
                  imageURI="images/ABC_Murder.jpg")
uwi7.item = detective1
user.items.append(uwi7)
detective.items.append(detective1)

session.commit()

uwi8 = user_with_item()
refer8 = References(rlink="https://en.wikipedia.org/wiki/"
                    "Nemesis_(Christie_novel)")
detective2 = Item(name="Nemesis",
                  description=dedent("""
                  Miss Marple receives a post card from the
                  recently deceased Jason Rafiel, a millionaire whom she had
                  met during a holiday on which she had encountered a murder,
                  which asks her to look into an unspecified crime; if she
                  succeeds in solving the crime, she will inherit £20,000.
                  Rafiel has left her few clues. She begins by joining a tour
                  of famous British houses and gardens with fifteen other
                  people, arranged by Mr Rafiel prior to his death. Elizabeth
                  Temple is the retired school headmistress who relates the
                  story of Verity, who was engaged to Rafiel's ne'er-do-well
                  son, Michael, but the marriage did not happen. Another,
                  member of the tour group, Miss Cooke, is a woman she had met
                  briefly in St Mary Mead."""),
                  refers=[refer8],
                  lastEditTime=datetime.now(),
                  imageURI="images/Nemesis.jpg")
uwi8.item = detective2
user.items.append(uwi8)
detective.items.append(detective2)

session.commit()

uwi9 = user_with_item()
detective3 = Item(name="Murder on the Orient Express",
                  description=dedent("""
                  When M. Bouc reaches his destination in Italy
                  on the second night of the journey, he gives up his first-
                  class compartment to Poirot, who is going on to Calais. That
                  compartment adjoins Ratchett’s. The train is stopped by a
                  snowdrift near Vincovci (sic). Among the several events that
                  disturb Poirot's sleep is a cry from Ratchett's compartment.
                  The next morning, M. Bouc informs him that Ratchett has been
                  murdered and asks Poirot to investigate."""),
                  lastEditTime=datetime.now(),
                  imageURI="images/Murder_On_the_Orient_Express.jpg")
uwi9.item = detective3
user.items.append(uwi9)
detective.items.append(detective3)

session.commit()

uwi10 = user_with_item()
detective4 = Item(name="And Then There Were None",
                  description=dedent("""
                  In the novel, a group of people are lured
                  into coming to an island under different pretexts, e.g.,
                  offers of employment, to enjoy a late summer holiday, or to
                  meet old friends. All have been complicit in the deaths of
                  other human beings, but either escaped justice or committed
                  an act that was not subject to legal sanction. The guests
                  and two servants who are present are "charged" with their
                  respective "crimes" by a gramophone recording after dinner
                  the first night, and informed that they have been brought to
                  the island to pay for their actions. They are the only,
                  people on the island, and cannot escape due to the distance
                  from the mainland and the inclement weather, and gradually
                  all ten are killed in turn, each in a manner that seems to
                  parallel the deaths in the nursery rhyme. Nobody else seems
                  to be left alive on the island by the time of the apparent
                  last death. A confession, in the form of a postscript to the
                  novel, unveils how the killings took place and who was
                  responsible."""),
                  lastEditTime=datetime.now())
uwi10.item = detective4
user.items.append(uwi10)
detective.items.append(detective4)

session.commit()
