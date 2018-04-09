#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category, User, DB_CONN_URI


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

anime1 = Item(name='君の名は(Your Name)',
              description="""Your Name tells the story of a high school girl
              in rural Japan and a high school boy in Tokyo who swap bodies.
              """,
              imageURI="images/Kimi_No_Namae_Wa.png",
              lastEditTime=datetime.now(),
              user=user,
              category=anime)


session.add(anime1)
session.commit()

anime2 = Item(name='あの日見た花の名前を僕達はまだ知らない(AnoHana)',
              description="""It is revealed that all of the group members
              blame themselves for Menma's death and long-hidden feelings are
              rekindled. The group struggles as they grow from trying to help
              Menma move on and help each other move on as well.
              """,
              imageURI="images/AnoHana.jpg",
              lastEditTime=datetime.now(),
              user=user,
              category=anime)


session.add(anime2)
session.commit()

anime3 = Item(name="四月は君の嘘(Your Lie in April)",
              description="""Much to everyone's sadness, Kaori dies due to the
              surgery, but leaves a letter to Kōsei which is given to him  by
              her parents at her funeral in which she eventually states that
              she was in love with Kōsei the whole time, and she lied  that
              she had a crush on Watari to get closer to him while not hurting
              Tsubaki's (who also has a crush on Kōsei) feelings. This was her
              lie: a lie she told in April.""",
              imageURI="images/Your_Lie_In_April.jpg",
              lastEditTime=datetime.now(),
              user=user,
              category=anime)

session.add(anime3)
session.commit()

anime4 = Item(name="花咲くいろは(The Blooming Colors)",
              description="""Initially feeling discouraged, she decides to use
              her circumstances as an opportunity to change herself for the
              better and to make amends with her deteriorating relationship
              with the Kissuisō's staff for a more prominent future.""",
              imageURI="images/The_Blooming_Colors.jpg",
              lastEditTime=datetime.now(),
              user=user,
              category=anime)

session.add(anime4)
session.commit()

anime5 = Item(name="とある科学の超電磁砲 レールガン(A Certain Scientific Railgun)",
              description="""In the futuristic Academy City, which is made up
              of 80% students, many of whom are espers possessing unique
              psychic powers, Mikoto Misaka is an electromaster who is the
              third strongest of a mere seven espers who have been given the
              rank of Level 5. The series focuses on the exploits of Mikoto
              and her friends; Kuroko Shirai, Kazari Uiharu, and Ruiko Saten,
              prior to and during the events of A Certain Magical Index.""",
              imageURI="images/A_Certain_Scientific_Railgun.jpg",
              lastEditTime=datetime.now(),
              user=user,
              category=anime)

session.add(anime5)
session.commit()

anime6 = Item(name="氷菓(Hyouka)",
              description="""At the request of his older sister, student Hotaro
              Oreki joins Kamiyama High School's Classic Literature Club to
              stop it from being abolished, joined by fellow members Eru
              Chitanda, Satoshi Fukube and Mayaka Ibara. The story is set in
              Kamiyama City, a fictional city in Gifu Prefecture that the
              author based on his real hometown of Takayama, also in Gifu. The
              fictional Kamiyama High School is based upon the real life Hida
              High School. They begin to solve various mysteries, both to help
              with their club and at Eru's requests.""",
              lastEditTime=datetime.now(),
              user=user,
              category=anime)

session.add(anime6)
session.commit()


# Category Detectives
detective = Category(name="Mysterious & Detectives")

detective1 = Item(name="The A.B.C. Murders",
                  description="""Returning from South America, Arthur Hastings
                  meets with his old friend Hercule Poirot, at his new flat in
                  London. Poirot shows him a mysterious letter he received,
                  signed "A.B.C.", that details a crime that is to be
                  committed very soon in August, which he suspects will be a
                  murder. Two more letters of the same nature soon arrive to
                  his flat, each prior to a murder being carried out by A.B.C.,
                  and done in alphabetical order: Alice Ascher, killed in her
                  tobacco shop in Andover; Elizabeth "Betty" Barnard, a flirty
                  waitress killed on the beach at Bexhill; and Sir Carmichael
                  Clarke, a wealthy man killed at his home in Churston. In
                  each murder, an ABC railway guide is left beside the victim.
                  """,
                  lastEditTime=datetime.now(),
                  imageURI="images/ABC_Murder.jpg",
                  user=user,
                  category=detective)

session.add(detective1)
session.commit()

detective2 = Item(name="Nemesis",
                  description="""Miss Marple receives a post card from the
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
                  briefly in St Mary Mead.""",
                  lastEditTime=datetime.now(),
                  imageURI="images/Nemesis.jpg",
                  user=user,
                  category=detective)

session.add(detective2)
session.commit()

detective3 = Item(name="Murder on the Orient Express",
                  description="""When M. Bouc reaches his destination in Italy
                  on the second night of the journey, he gives up his first-
                  class compartment to Poirot, who is going on to Calais. That
                  compartment adjoins Ratchett’s. The train is stopped by a
                  snowdrift near Vincovci (sic). Among the several events that
                  disturb Poirot's sleep is a cry from Ratchett's compartment.
                  The next morning, M. Bouc informs him that Ratchett has been
                  murdered and asks Poirot to investigate.""",
                  lastEditTime=datetime.now(),
                  imageURI="images/Murder_On_the_Orient_Express.jpg",
                  user=user,
                  category=detective)

session.add(detective3)
session.commit()

detective4 = Item(name="And Then There Were None",
                  description="""In the novel, a group of people are lured
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
                  responsible.""",
                  lastEditTime=datetime.now(),
                  user=user,
                  category=detective)
