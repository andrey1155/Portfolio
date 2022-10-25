/*

#pragma once
#include <SFML/Graphics.hpp>
#include <string>
#include <vector>
#include "VectAlg.h"
#include "Plane.h"

using namespace alg;
using namespace sf;
class RigidBody2D;
class RenderVector2D;
class Plane;
class Engine2D
{
private:

	std::vector<RenderVector2D*> vectors;
	RenderWindow window;
	

public:
	Engine2D();
	void addVector(alg::Vector2 vect, alg::Vector2 pos);
	void startEngine();
	RigidBody2D body;
};

class RenderVector2D {
public:
	RenderVector2D(alg::Vector2, alg::Vector2);
	RenderVector2D(void);
	RectangleShape toRender;
private:
	alg::Vector2 pos;
	alg::Vector2 vect;	
};

struct Force {
	alg::Vector2* force, *point;
	Force() { force = &alg::Vector2(); point = &alg::Vector2(); }
	Force(alg::Vector2* a, alg::Vector2* b) { force = a; point = b; }
};

class RigidBody2D {
private:
	float A,B;
	float mass, I;
	sf::Vector2f massCenter;
	float E, W, Fi;
	alg::Vector2 a, v, r;
	std::vector<Force*> constForces;
public:
	RectangleShape toRender;
	RigidBody2D(float,float,alg::Vector2, alg::Vector2, alg::Vector2, float, float, float);
	void addForce(alg::Vector2*, alg::Vector2*);
	void update(float);
};
*/