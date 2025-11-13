# Vehicle Parking App – V2

**Project for:** Modern Application Development II (MAD II) – May 2025  
**Technologies Used:** Flask, VueJS, Bootstrap, SQLite, Redis, Celery  

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Roles](#roles)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Folder Structure](#folder-structure)  
7. [Database Design](#database-design)  
8. [API Endpoints](#api-endpoints)  
9. [Scheduled Jobs & Async Tasks](#scheduled-jobs--async-tasks)  
10. [Additional Features](#additional-features)  
11. [Video Demonstration](#video-demonstration)  

---

## Project Overview
Vehicle Parking App – V2 is a multi-user application that manages parking lots, parking spots, and vehicles for 4-wheelers.  
The system supports **Admin** and **User** roles, with full control over parking lot operations for admins, and easy spot booking for users.  

**Purpose:**  
- Simplify parking management  
- Provide automated spot allocation  
- Generate reports and reminders  

---

## Features

### Admin
- Single superuser with root access  
- Create, edit, delete parking lots  
- Set number of parking spots per lot automatically  
- View parked vehicle details and parking spot status  
- View summary charts of parking lots and users  

### User
- Register/Login  
- Reserve the first available parking spot in a lot  
- Change parking spot status to occupied/released  
- View parking history and summary charts  
- Export parking data as CSV  

---

## Roles
| Role  | Access |
|-------|--------|
| Admin | Superuser; create/edit/delete lots; manage spots; view users and stats |
| User  | Book/release spots; view parking history; export data |

---

## Installation

### Prerequisites
- Python 3.x  
- Node.js & npm (for VueJS frontend)  
- Redis  
- SQLite (built-in with Python)  
