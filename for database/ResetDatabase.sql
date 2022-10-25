DROP DATABASE IF EXISTS  plane_model_results;
CREATE DATABASE plane_model_results;

USE plane_model_results;

CREATE TABLE run_1 (
	t float4,
    A float4,
    B float4,
    Cch float4,
    East float4,
    H float4,
    Hch float4,
    Heading float4,
    North float4,
    Pitch float4,
    R float4,
    Roll float4,
    Speed float4,
    Theta float4,
    Yaw float4
);