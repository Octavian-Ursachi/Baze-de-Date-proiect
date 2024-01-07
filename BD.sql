BEGIN
   BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE intersection CASCADE CONSTRAINTS';
   EXCEPTION
      WHEN OTHERS THEN
         IF SQLCODE != -942 THEN
            RAISE;
         END IF;
   END;
   

   BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE i_lanes CASCADE CONSTRAINTS';
   EXCEPTION
      WHEN OTHERS THEN
         IF SQLCODE != -942 THEN
            RAISE;
         END IF;
   END;

   BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE traffic_lanes CASCADE CONSTRAINTS';
   EXCEPTION
      WHEN OTHERS THEN
         IF SQLCODE != -942 THEN
            RAISE;
         END IF;
   END;

   BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE vehicles CASCADE CONSTRAINTS';
   EXCEPTION
      WHEN OTHERS THEN
         IF SQLCODE != -942 THEN
            RAISE;
         END IF;
   END;

   BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE weather_conditions CASCADE CONSTRAINTS';
   EXCEPTION
      WHEN OTHERS THEN
         IF SQLCODE != -942 THEN
            RAISE;
         END IF;
   END;

   BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE i_events CASCADE CONSTRAINTS';
   EXCEPTION
      WHEN OTHERS THEN
         IF SQLCODE != -942 THEN
            RAISE;
         END IF;
   END;
END;


create table intersections(
        intersection_id NUMBER(4),
        intersection_name VARCHAR2(30),
        intersection_location VARCHAR2(30),
        traffic_control_type VARCHAR2(30),
        maximum_speed_limit NUMBER(4),
        constraint intersection_ccj_pk PRIMARY KEY (intersection_id)
        );
        
INSERT INTO intersection(intersection_id, intersection_name, intersection_location, traffic_control_type, maximum_speed_limit)
values(0,'City_Center_Junction','Downtown','Traffic_lights',50);
        
INSERT INTO intersection(intersection_id, intersection_name, intersection_location, traffic_control_type, maximum_speed_limit)
values(1,'Tudor_junction','Downtown','Traffic_lights',50);

INSERT INTO intersection(intersection_id, intersection_name, intersection_location, traffic_control_type, maximum_speed_limit)
values(2,'Mall_Junction','City_centre','Traffic_lights',30);

INSERT INTO intersection(intersection_id, intersection_name, intersection_location, traffic_control_type, maximum_speed_limit)
values(3,'Small_junction','Outskirts','None',50);

INSERT INTO intersection(intersection_id, intersection_name, intersection_location, traffic_control_type, maximum_speed_limit)
values(4,'Busy_junction','Downtown','Many_traffic_lights',40);

create table traffic_lanes(
        lane_id NUMBER(4),
        lane_type VARCHAR2(50),
        traffic_direction VARCHAR2(50),
        intersection_id NUMBER(4),
        constraint traffic_lanes_intersection_id_fk FOREIGN KEY(intersection_id) REFERENCES intersection(intersection_id),
        constraint traffic_lanes_traffic_direction_ck CHECK (traffic_direction IN ('southbound','northbound','westbound','eastbound'))
        );
        
INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (1, 'Through_Lane', 'northbound', 0);

INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (2, 'Right-Turn_Lane', 'southbound', 0);

INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (3, 'Left-Turn_Lane', 'eastbound', 1);

INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (4, 'Through_Lane', 'westbound', 1);

INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (5, 'Right-Turn_Lane', 'northbound', 2);

INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (6, 'Left-Turn_Lane', 'southbound', 2);

INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (7, 'Through_Lane', 'eastbound', 3);

INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (8, 'Right-Turn_Lane', 'westbound', 3);

INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (9, 'Left-Turn_Lane', 'northbound', 4);

INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (10, 'Through_Lane', 'southbound', 4);

INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (11, 'Right-Turn_Lane', 'eastbound', 0);

INSERT INTO traffic_lanes (lane_id, lane_type, traffic_direction, intersection_id)
VALUES (0, 'Left-Turn_Lane', 'westbound', 0);



create table vehicles(
        vehicle_id NUMBER(4),
        vehicle_type VARCHAR2(10),
        speed NUMBER(3), 
        direction VARCHAR2(15),
        intersection_id NUMBER(4),
        constraint vehicles_vehicle_id_pk PRIMARY KEY (vehicle_id),
        constraint vehicles_lane_fk FOREIGN KEY(lane_id) REFERENCES traffic_lanes(lane_id),
        constraint direction_ck CHECK (direction IN ('southbound','northbound','westbound','eastbound'))
        );
        
INSERT INTO vehicles (vehicle_id, vehicle_type, speed, direction, (lane_id),
VALUES (1, 'Car', 60, 'northbound', 1);

INSERT INTO vehicles (vehicle_id, vehicle_type, speed, direction, (lane_id),
VALUES (2, 'Truck', 45, 'southbound', 0);

INSERT INTO vehicles (vehicle_id, vehicle_type, speed, direction, (lane_id),
VALUES (3, 'Motorcycle', 80, 'eastbound', 3);

INSERT INTO vehicles (vehicle_id, vehicle_type, speed, direction, (lane_id),
VALUES (4, 'Bicycle', 20, 'westbound', 2);

INSERT INTO vehicles (vehicle_id, vehicle_type, speed, direction, (lane_id),
VALUES (5, 'Bus', 55, 'northbound', 4);

INSERT INTO vehicles (vehicle_id, vehicle_type, speed, direction, (lane_id),
VALUES (6, 'Car', 65, 'southbound', 5);

INSERT INTO vehicles (vehicle_id, vehicle_type, speed, direction, (lane_id),
VALUES (7, 'Truck', 40, 'eastbound', 1);

INSERT INTO vehicles (vehicle_id, vehicle_type, speed, direction, (lane_id),
VALUES (8, 'Motorcycle', 75, 'westbound', 7);

INSERT INTO vehicles (vehicle_id, vehicle_type, speed, direction, (lane_id),
VALUES (9, 'Bicycle', 15, 'northbound', 9);

INSERT INTO vehicles (vehicle_id, vehicle_type, speed, direction, (lane_id),
VALUES (10, 'Bus', 50, 'southbound', 10);


        
create table weather_conditions(
        intersection_id NUMBER(4),
        temperature NUMBER(2),
        precipitation VARCHAR2(50),
        wind_speed NUMBER(3),
        constraint weather_intersection_id_fk FOREIGN KEY(intersection_id) REFERENCES intersection(intersection_id),
        constraint uq_weather_intersection_id UNIQUE (intersection_id)
        );
        
INSERT INTO weather_conditions (intersection_id, temperature, precipitation, wind_speed)
VALUES (0, 25, 'Light_Rain', 10);
        
INSERT INTO weather_conditions (intersection_id, temperature, precipitation, wind_speed)
VALUES (1, 27, 'Cloudy', 16);

INSERT INTO weather_conditions (intersection_id, temperature, precipitation, wind_speed)
VALUES (2, 21, 'Thick_Fog', 2);

INSERT INTO weather_conditions (intersection_id, temperature, precipitation, wind_speed)
VALUES (3, 29, 'Sunny', 7);

INSERT INTO weather_conditions (intersection_id, temperature, precipitation, wind_speed)
VALUES (4, 20, 'Downpour', 24);

create table i_events(
        event_id NUMBER(4),
        event_type VARCHAR2(50),
        event_description VARCHAR2(255),
        event_time TIMESTAMP,
        intersection_id NUMBER(4),
        constraint event_intersection_id_fk FOREIGN KEY(intersection_id) REFERENCES intersection(intersection_id)
        );
        
INSERT INTO i_events (event_id, event_type, event_description, event_time, intersection_id)
VALUES (1, 'Accident', 'Vehicle collision at the intersection', TO_TIMESTAMP('2023-01-15 08:30:00', 'YYYY-MM-DD HH24:MI:SS'), 1);

INSERT INTO i_events (event_id, event_type, event_description, event_time, intersection_id)
VALUES (2, 'Construction', 'Road construction causing lane closures', TO_TIMESTAMP('2023-02-20 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 0);

INSERT INTO i_events (event_id, event_type, event_description, event_time, intersection_id)
VALUES (3, 'Protest', 'Street protest affecting traffic flow', TO_TIMESTAMP('2023-03-10 15:45:00', 'YYYY-MM-DD HH24:MI:SS'), 2);

INSERT INTO i_events (event_id, event_type, event_description, event_time, intersection_id)
VALUES (4, 'Road_Closure', 'Scheduled road closure for maintenance', TO_TIMESTAMP('2023-04-05 22:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3);

INSERT INTO i_events (event_id, event_type, event_description, event_time, intersection_id)
VALUES (5, 'Traffic_Signal_Failure', 'Malfunctioning traffic signals at the intersection', TO_TIMESTAMP('2023-05-12 13:20:00', 'YYYY-MM-DD HH24:MI:SS'), 4);

SELECT * FROM intersection;

SELECT * FROM traffic_lanes;

SELECT * FROM vehicles;

SELECT * FROM weather_conditions;

SELECT * FROM i_events;


        
        
        