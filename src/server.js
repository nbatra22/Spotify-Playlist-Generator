import express from 'express';
import path from 'path';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';

dotenv.config();

const app = express();
const port = 3000;

const developerToken = process.env.DEVELOPER_TOKEN;
const userToken = process.env.USER_TOKEN;  // Get user token from .env file

// const initialDirname = path.dirname(new URL(import.meta.url).pathname);
// let processedDirname = initialDirname.startsWith('/') ? initialDirname.slice(1) : initialDirname; // removes the leading /
// processedDirname = processedDirname.endsWith("/src") ? processedDirname.slice(0, -4) : processedDirname; // removes the /src from the end
// const __dirname = decodeURIComponent(processedDirname); // decodes the URI encoding

const __filename = fileURLToPath (import.meta.url);
const __dirname = path.dirname(__filename); // Correctly extracts the directory
  // Serve static files from the /client directory
app.use(express.static(path.join(__dirname, 'client')));

// Endpoint to handle the login API (using the userToken from .env file)
app.post('/api/login', (req, res) => {
  if (!userToken) {
    return res.status(400).json({ error: 'User token not available' });
  }

  console.log('Using user token from .env:', userToken);  // Process token (you can store/validate it)
  res.status(200).json({ message: 'Login successful with token from .env file' });
});

app.get('*', (req, res) => {
  res. sendFile(path.join(__dirname, '../client/index.html'));
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

export default app;