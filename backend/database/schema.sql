-- PostgreSQL DDL for EmptyMug Contact Form
-- This file contains the database schema for storing contact form submissions

-- Create database (run this manually if needed)
-- CREATE DATABASE emptymug;

-- Connect to the emptymug database
-- \c emptymug;

-- Create contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    country_code VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email);
CREATE INDEX IF NOT EXISTS idx_contacts_created_at ON contacts(created_at);
CREATE INDEX IF NOT EXISTS idx_contacts_country_code ON contacts(country_code);

-- Create function to automatically update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
DROP TRIGGER IF EXISTS update_contacts_updated_at ON contacts;
CREATE TRIGGER update_contacts_updated_at
    BEFORE UPDATE ON contacts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE contacts IS 'Stores contact form submissions from the EmptyMug website';
COMMENT ON COLUMN contacts.id IS 'Unique identifier for each contact submission';
COMMENT ON COLUMN contacts.full_name IS 'Full name of the person submitting the form';
COMMENT ON COLUMN contacts.email IS 'Email address of the person submitting the form';
COMMENT ON COLUMN contacts.phone_number IS 'Optional phone number';
COMMENT ON COLUMN contacts.country_code IS 'Country code for the phone number';
COMMENT ON COLUMN contacts.message IS 'The message content from the contact form';
COMMENT ON COLUMN contacts.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN contacts.updated_at IS 'Timestamp when the record was last updated';
