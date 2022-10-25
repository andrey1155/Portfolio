#pragma once

#include <math.h>

namespace alg {

	class Vector3 {

	public:

		Vector3() : x(0), y(0), z(0) {}
		Vector3(float x, float y, float z) : x(x),y(y),z(z) {}

		float x, y, z;

	};

	class Vector2 {

	public:

		Vector2(float x, float y) : x(x),y(y) { }
		Vector2() : x(0), y(0) { }
		float x, y;

	};

	class Matrix3x3 {

	public:
		Matrix3x3(float a1, float a2, float a3,
				  float b1, float b2, float b3,
				  float c1, float c2, float c3 ) {

			m[0][0] = a1;
			m[0][1] = a2;
			m[0][2] = a3;

			m[1][0] = b1;
			m[1][1] = b2;
			m[1][2] = b3;

			m[2][0] = c1;
			m[2][1] = c2;
			m[2][2] = c3;

		}

		float m[3][3];
	};


	Vector3 operator*(const Vector3& v, float n);

	Vector3 operator-(const Vector3& v1, const Vector3& v2);

	Vector3 operator+(const Vector3& v1, const Vector3& v2);

	Vector2 operator*(const Vector2& v, float n);

	Vector3 operator*(const Matrix3x3& m, const Vector3& v);

	Matrix3x3 createTurnMatrix90(Vector3 v);

	Vector2 showXY(Vector3 v);

	Vector2 showXZ(Vector3 v);

	Vector2 showYZ(Vector3 v);


	float abs(Vector3 v);

	float abs(Vector2 v);

	Vector3 getNormalized(Vector3 v);

}