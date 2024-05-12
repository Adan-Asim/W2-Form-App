
# W2-FORM-CHAT

## Overview
This project is a full-stack application using Flask and Python for the backend and Next.js powered by React for the frontend. It allows users to upload files and interact with the file data through a series of queries. The interface is styled with Tailwind CSS for a responsive design, along with html and css.

## Features
- Allow users to signup/login on the App.
- Allow users to upload files in any format like pdf, jpg, jpeg etc.
- Allow data querying to answer user questions based on file data.
- Maintain record of previous user data including files and chat histories as well.
- Have encryption for storing file data securely in DB and also show sensitive data after password confirmation.
- Fully Responsive web interface using Next.js and Tailwind CSS.

## Technology Stack
- **Backend:** Flask, Python
- **Frontend:** Next.js, React, Tailwind CSS, TS
- **Database:** PostgreSQL, SQLAlchemy
- **LLMs:** ChatGPT gpt-3.5, Gorq (llama)

## Getting Started

### Prerequisites
Ensure you have the following installed:
- Docker
- Node.js (version 14 or higher)
- Python (version 3.9 or higher)

### Setup Instructions

#### Backend Setup
Navigate to the backend directory:
```bash
cd backend
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Start the backend server:
```bash
flask run
```

#### Frontend Setup
Navigate to the frontend directory:
```bash
cd frontend
```

Install JavaScript dependencies:
```bash
npm install
```

Run the development server:
```bash
npm run dev
```

### Using Docker
To run the entire application using Docker:
```bash
docker-compose up --build
```

## Deployment
Deployed on following URL: https://form-chat-frontend-aw3wvc3u4-adans-projects-962d6816.vercel.app/

## Usage
You just need to signup and then can start using the app.

## Contributing
Contributions are welcome. Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your-project/tags).

## Authors
- **Adan Asim** - *Initial work* - [GithubProfile](https://github.com/adan-asim)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

