/*

#include "Engine2D.h"
#include <math.h>
#include <iostream>

Engine2D::Engine2D() : body(300.f,70.f,alg::Vector2(400,400),alg::Vector2(),alg::Vector2(),10,0,0)
{
	window.create(sf::VideoMode(700, 700), "RocketShot");
}

void Engine2D::startEngine()
{
	Clock clock;

	while (window.isOpen())
	{
		Time _dt_ = clock.getElapsedTime();
		Int32 dt = _dt_.asMilliseconds();
		
		
		if (dt > 1) {
			body.update(dt);
			clock.restart();		
		}

		

		sf::Event event;

		while (window.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
				window.close();
		}
		
		window.draw(body.toRender);
		window.display();
		window.clear();
	}
}

RenderVector2D::RenderVector2D(alg::Vector2 vect, alg::Vector2 pos) {
	this->vect = vect;
	this->pos = pos;

	toRender = RectangleShape(Vector2f(sqrt(vect.x*vect.x + vect.y*vect.y), 1.f));
	toRender.setPosition(Vector2f(pos.x,pos.y));
	if (vect.x != 0) {
		if(vect.x<0)
			toRender.rotate(180 / 3.14*atan(vect.y / vect.x)+180);
		else toRender.rotate(180 / 3.14*atan(vect.y / vect.x));
	}
	else if (vect.y > 0)
		toRender.rotate(-90);
	else if (vect.y < 0)
		toRender.rotate(90);
}

void Engine2D::addVector(alg::Vector2 vect, alg::Vector2 pos) {
	this->vectors.push_back(new RenderVector2D(vect,pos));
}

RenderVector2D::RenderVector2D(void) {
	pos = alg::Vector2(0.f, 0.f);
	vect = alg::Vector2(0.f, 0.f);
	toRender = RectangleShape(Vector2f(0.f, 0.f));
}
*/