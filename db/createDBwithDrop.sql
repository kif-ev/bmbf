### Drop Order ###
drop table bmbf__times;
drop table bmbf__participants;
drop table bmbf__mapping;
drop table bmbf__auth;
drop table bmbf__groups;
drop table bmbf__events;
drop table bmbf__templates;


create table bmbf__templates
(
	id int auto_increment,
	filename mediumtext not null,
	constraint bmbf__templates_pk
		primary key (id)
);


create table bmbf__events
(
	id int auto_increment,
	organization mediumtext not null,
	measure mediumtext not null,
	template int not null,
	measure_periode mediumtext not null,
	constraint bmbf__events_bmbf__templates_id_fk
		foreign key (template) references bmbf__templates (id),
	constraint bmbf__events_pk
		primary key (id)
);

create table bmbf__groups
(
    event    int not null,
    group_id MEDIUMTEXT not null,
    ugid     int auto_increment,
    constraint bmbf__groups_pk
		primary key (ugid),
    constraint bmbf__groups_bmbf__events_id_fk
        foreign key (event) references bmbf__events (id)
);


create table bmbf__participants
(
    id         int        auto_increment,
    event      int        not null,
    name       mediumtext not null,
    university mediumtext not null,
    grp int null,
    constraint bmbf__articipants_bmbf__events_id_fk
        foreign key (event) references bmbf__events (id),
    constraint bmbf__participants_bmbf__groups_ugid_fk
		foreign key (grp) references bmbf__groups (ugid),
    constraint bmbf__participants_pk
		primary key (id)
);

create table bmbf__times
(
	event int not null,
	startdate date not null,
	enddate date not null,
	constraint bmbf__times_bmbf__events_id_fk
		foreign key (event) references bmbf__events (id)
);

create table bmbf__auth
(
	uid int auto_increment,
	token varchar(190) not null
);

create unique index bmbf__auth_key_uindex
	on bmbf__auth (token);

create table bmbf__mapping
(
	uid int not null,
	eid int not null,
	constraint bmbf__mapping_bmbf__auth_uid_fk
		foreign key (uid) references bmbf__auth (uid),
	constraint bmbf__mapping_bmbf__events_id_fk
		foreign key (eid) references bmbf__events (id)
);

create unique index bmbf__mapping_eid_uindex
	on bmbf__mapping (eid);