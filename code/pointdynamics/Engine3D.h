#pragma once
#include <SFML/Graphics.hpp>
#include <string>
#include <vector>
#include "VectAlg.h"
#include "Definitions.h"

using namespace alg;
using namespace sf;

class RigidBody;
class MaterialPoint;
class RenderVector;

class MaterialPoint {
public:
	alg::Vector3 r, v, a;
	std::vector<alg::Vector3> constForces;
	std::vector<alg::Vector3(*)(alg::Vector3, alg::Vector3, float)> funcForces;
	const float mass = 1;

	MaterialPoint(alg::Vector3, alg::Vector3, alg::Vector3);
	MaterialPoint(const MaterialPoint&);
	void addForce(alg::Vector3);
	void addForce(alg::Vector3(*v)(alg::Vector3, alg::Vector3,float));
	void update(float,float);
	void CheckBorderCollision(float*,float*,float,float);
};

class Engine
{
private:

	RenderWindow windowXY, windowXZ, windowYZ;
	MaterialPoint point;
	float time = 0;

	sf::Font font;
	sf::Text labels[4 * 3];

	void InitLabel(int, sf::Vector2f, std::string);
	void toXY(MaterialPoint*);
	void toXZ(MaterialPoint*);
	void toYZ(MaterialPoint*);
	void RenderPoint(sf::RenderWindow*, float, float);

public:

	Engine(MaterialPoint);
	void startEngine();
};



class RenderVector {
public:
	sf::RectangleShape line;
	sf::Vector2f pos;
	RenderVector(alg::Vector2,alg::Vector2);
	RenderVector(alg::Vector2, alg::Vector2, sf::Color);
};

void toXY(MaterialPoint*,Engine*);