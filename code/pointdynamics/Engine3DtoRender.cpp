#include "Engine3D.h"

#define UNIT_LENGTH 0.03
#define VELOCITY_UNIT_LENGTH 1

RenderVector::RenderVector(alg::Vector2 v,alg::Vector2 pos) {
	this->pos = Vector2f(pos.x,pos.y);
	line = RectangleShape(Vector2f(1.f, alg::abs(v)));
	line.setPosition(Vector2f(pos.x, pos.y));
	if (v.x != 0) {
		if (v.x < 0)
			line.rotate(180 / 3.14*atan(v.y / v.x) +90);
		else line.rotate(180 / 3.14*atan(v.y / v.x)-90);
	}
	else if (v.y > 0)
		line.rotate(0);
	else if (v.y < 0)
		line.rotate(180);
}

RenderVector::RenderVector(alg::Vector2 v, alg::Vector2 pos, sf::Color color) 
	: RenderVector(v, pos)
{
	line.setFillColor(color);
}

void Engine::RenderPoint(sf::RenderWindow* window, float a, float b) {
	sf::CircleShape pnt(12.f);
	pnt.setFillColor(sf::Color(100, 250, 50));
	pnt.setPosition(sf::Vector2f(a, b));
	pnt.setOrigin(sf::Vector2f(2.5, 2.5));
	window->draw(pnt);
}

void Engine::toXY(MaterialPoint* point) {

	for (int i = 0; i < 4; i++) {
		windowXY.draw(labels[i]);
	}

	RenderPoint(&windowXY, point->r.x, point->r.y);
	RenderVector velocity(alg::showXY(point->v) * VELOCITY_UNIT_LENGTH, alg::showXY(point->r), Color(255, 0, 0));
	windowXY.draw(velocity.line);

	for (int i = 0; i < point->constForces.size(); i++)
		windowXY.draw(RenderVector(alg::showXY(point->constForces.at(i))* UNIT_LENGTH, alg::showXY(point->r)).line);
	for (int i = 0; i < point->funcForces.size(); i++)
		windowXY.draw(RenderVector(alg::showXY(point->funcForces.at(i)(point->r, point->v, 0)) * UNIT_LENGTH, alg::showXY(point->r)).line);
}

void Engine::toXZ(MaterialPoint* point) {

	for (int i = 4; i < 8; i++) {
		windowXZ.draw(labels[i]);
	}

	RenderPoint(&windowXZ, point->r.x, point->r.z);
	RenderVector velocity(alg::showXZ(point->v) * VELOCITY_UNIT_LENGTH, alg::showXZ(point->r), Color(255, 0, 0));
	windowXZ.draw(velocity.line);
	
	for (int i = 0; i < point->constForces.size(); i++)
		windowXZ.draw(RenderVector(alg::showXZ(point->constForces.at(i)) * UNIT_LENGTH, alg::showXZ(point->r)).line);
	for (int i = 0; i < point->funcForces.size(); i++)
		windowXZ.draw(RenderVector(alg::showXZ(point->funcForces.at(i)(point->r, point->v, 0)) * UNIT_LENGTH, alg::showXZ(point->r)).line);
}

void Engine::toYZ(MaterialPoint* point) {

	for (int i = 8; i < 12; i++) {
		windowYZ.draw(labels[i]);
	}

	RenderPoint(&windowYZ, point->r.y, point->r.z);
	RenderVector velocity(alg::showYZ(point->v) * VELOCITY_UNIT_LENGTH, alg::showYZ(point->r), Color(255, 0, 0));
	windowYZ.draw(velocity.line);

	for (int i = 0; i < point->constForces.size(); i++)
		windowYZ.draw(RenderVector(alg::showYZ(point->constForces.at(i)) * UNIT_LENGTH, alg::showYZ(point->r)).line);
	for (int i = 0; i < point->funcForces.size(); i++)
		windowYZ.draw(RenderVector(alg::showYZ(point->funcForces.at(i)(point->r,point->v,0)) * UNIT_LENGTH, alg::showYZ(point->r)).line);
}