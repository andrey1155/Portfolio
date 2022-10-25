/*

#include "Engine2D.h"
#include "VectAlg.h"

RigidBody2D::RigidBody2D(float A, float B,alg::Vector2 r, alg::Vector2 v, alg::Vector2 a, float Fi, float W, float E) {
	this->r = r; this->v = v; this->a = a;
	this->Fi = Fi; this->W = W; this->E = E;
	this->A = A; this->B = B;
	this->massCenter = sf::Vector2f(A / 2, B / 2);
	toRender = RectangleShape(Vector2f(A, B));
	toRender.setOrigin(massCenter);
	toRender.setPosition(Vector2f(r.x, r.y));
	toRender.setRotation(Fi);
	toRender.setFillColor(sf::Color::White);
}

void RigidBody2D::addForce(alg::Vector2* force, alg::Vector2* point) {
	constForces.push_back(new Force(force, point));
}

void RigidBody2D::update(float dt) {
	alg::Vector2 R;
	float M = 0;
	for (int i = 0; i < constForces.size(); i++)
		R = R + *constForces.at(i)->force;

	a = R * (1 / mass);
	v = v + a * dt;
	r = r + v * dt;

	for (int i = 0; i < constForces.size(); i++)
	{
		float h = abs(*constForces.at(i)->point)*sin(getAngle(*constForces.at(i)->point, *constForces.at(i)->force));
		M += h * abs(*constForces.at(i)->force);
	}

	E = M / I;
	W += E * dt; Fi += W * dt;
}

*/