#include "Engine3D.h"
#include <iostream>

MaterialPoint::MaterialPoint(alg::Vector3 R, alg::Vector3 V, alg::Vector3 A) {
	r = R;
	v = V;
	a = A;
}

MaterialPoint::MaterialPoint(const MaterialPoint& mp):
	constForces(mp.constForces), funcForces(mp.funcForces)
{
	r = mp.r;
	v = mp.v;
	a = mp.a;
}


void MaterialPoint::addForce(alg::Vector3 v) {
	constForces.push_back(v);
}

void MaterialPoint::addForce(alg::Vector3(*v)(alg::Vector3, alg::Vector3, float)) {
	funcForces.push_back(v);
}

void MaterialPoint::update(float dt, float time) {
	alg::Vector3 R;
	for (int i = 0; i < constForces.size() ; i++)
		R = R + constForces.at(i);
	for (int i = 0; i < funcForces.size(); i++)
		R = R + funcForces.at(i)(r,v,time);

	a = R*(1/mass)  * dt;
	v = v + a * dt;
	r = r + v * dt;

	std::cout << abs(v) << std::endl;

	CheckBorderCollision(&r.x,&v.x,0,WIDTH);
	CheckBorderCollision(&r.y, &v.y, 0, WIDTH);
	CheckBorderCollision(&r.z, &v.z, 0, WIDTH);
}

void MaterialPoint::CheckBorderCollision(float* X, float* V, float boundLow, float boundHigh) {

	if (*X < boundLow)
	{
		*X = boundLow;
		*V = -(*V)*0.9;
		return;
	}

	if (*X > boundHigh)
	{
		*X = boundHigh;
		*V = -(*V) * 0.9;
	}
}