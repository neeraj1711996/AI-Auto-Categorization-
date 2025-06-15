
AI Auto Categorisation with Gemini API
This project provides a simple graphical user interface (GUI) application built with Tkinter that leverages the Google Gemini 1.5 Pro API for automatic item categorization, subcategorization, and attribute extraction based on a text description and an image input. This tool acts as an "Auction House" categorizer, aiming to streamline the process of listing items by intelligently suggesting relevant classifications and attributes.

Features
Image Upload: Select and upload an image file (e.g., JPG, PNG) for analysis.
Text Input: Provide a textual description or title for the item.
Gemini 1.5 Pro Integration: Utilizes the advanced multi-modal capabilities of the Gemini 1.5 Pro model to understand both text and image context.
Dynamic Categorization: The model acts as an "Auction House" to categorize items into one or more categories and subcategories.
The application takes an image and a text input from the user. These inputs are then sent to the Google Gemini 1.5 Pro API. A carefully crafted prompt guides the Gemini model to act as an "Auction House" and perform the following tasks:

Category Identification: Determine the primary and any additional relevant categories for the item.
Subcategory Assignment: Assign one or more subcategories within the identified main categories.
Attribute Listing: Extract and list attributes pertinent to the item, matching them against a conceptual pre-defined list of attributes for each category.
The API's response, containing the categorized data, is then displayed in the application's response box.

Prerequisites
Before running the application, ensure you have the following:

Python 3.7+
Google Gemini API Key: You can obtain one from the Google AI Studio.
Required Python Libraries:
google-generativeai
tkinter (usually comes pre-installed with Python)
