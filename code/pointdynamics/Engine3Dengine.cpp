#include "Engine3D.h"
#include <string>;
#include <cstdlib>

void Engine::InitLabel(int id, sf::Vector2f pos, std::string text) {

	labels[id].setFont(font);
	labels[id].setString(text);
	labels[id].setCharacterSize(FONT_SIZE);
	labels[id].setFillColor(sf::Color::White);
	labels[id].setPosition(pos);
}

Engine::Engine(MaterialPoint p)
	: point(p)
{
	if (!font.loadFromFile("arial.ttf"))
	{
		throw "Where is my font?";
	}

	windowXY.create(sf::VideoMode(WIDTH, HEIGHT), "XY");
	InitLabel(0, sf::Vector2f(WIDTH - HORIZONTAL_BORDER_OFFSET_RIGHT,HEIGHT/2), "+X");
	InitLabel(1, sf::Vector2f(HORIZONTAL_BORDER_OFFSET_LEFT, HEIGHT / 2), "-X");
	InitLabel(2, sf::Vector2f(WIDTH/2 - 2*FONT_SIZE, VERTICAL_BORDER_OFFSET), "-Y");
	InitLabel(3, sf::Vector2f(WIDTH/2 - 2*FONT_SIZE, HEIGHT - VERTICAL_BORDER_OFFSET-FONT_SIZE), "+Y");
	windowXY.setPosition(sf::Vector2i(WIDTH*0, 0));

	windowXZ.create(sf::VideoMode(WIDTH, HEIGHT), "XZ");
	InitLabel(4, sf::Vector2f(WIDTH - HORIZONTAL_BORDER_OFFSET_RIGHT, HEIGHT / 2), "+X");
	InitLabel(5, sf::Vector2f(HORIZONTAL_BORDER_OFFSET_LEFT, HEIGHT / 2), "-X");
	InitLabel(6, sf::Vector2f(WIDTH / 2 - 2 * FONT_SIZE, VERTICAL_BORDER_OFFSET), "-Z");
	InitLabel(7, sf::Vector2f(WIDTH / 2 - 2 * FONT_SIZE, HEIGHT - VERTICAL_BORDER_OFFSET - FONT_SIZE), "+Z");
	windowXZ.setPosition(sf::Vector2i(WIDTH*1, 0));

	windowYZ.create(sf::VideoMode(WIDTH, HEIGHT), "YZ");
	InitLabel(8, sf::Vector2f(WIDTH - HORIZONTAL_BORDER_OFFSET_RIGHT, HEIGHT / 2), "+Y");
	InitLabel(9, sf::Vector2f(HORIZONTAL_BORDER_OFFSET_LEFT, HEIGHT / 2), "-Y");
	InitLabel(10, sf::Vector2f(WIDTH / 2 - 2 * FONT_SIZE, VERTICAL_BORDER_OFFSET), "-Z");
	InitLabel(11, sf::Vector2f(WIDTH / 2 - 2 * FONT_SIZE, HEIGHT - VERTICAL_BORDER_OFFSET - FONT_SIZE), "+Z");

	windowYZ.setPosition(sf::Vector2i(WIDTH*2, 0));
}

void Engine::startEngine()
{
	//Clock clock;

	while (windowXY.isOpen() && windowXZ.isOpen() && windowYZ.isOpen())
	{
		//Time dt1 = clock.getElapsedTime();

		//if (dt1.asMicroseconds() < 1000)
		//	continue;

		//float dt = dt1.asMicroseconds() / 1000000.f;
		float dt = 0.01;

		if (dt > 0.5)
			throw "Invalid dt";

		time += dt;

		//clock.restart();
		point.update(dt,time);


		sf::Event event;

		while (windowXY.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
				windowXY.close();
		}
		while (windowYZ.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
				windowXY.close();
		}
		while (windowXZ.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
				windowXY.close();
		}
		while (windowYZ.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
				windowXY.close();
		}

		toXY(&point);
		toXZ(&point);
		toYZ(&point);

		windowXY.display();
		windowXY.clear();
		windowXZ.display();
		windowXZ.clear();
		windowYZ.display();
		windowYZ.clear();

	}
}

