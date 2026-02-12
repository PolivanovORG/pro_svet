# TODO List - Features from Technical Specification Not Yet Implemented

Based on the technical specification in README.md, the following features still need to be implemented:

## System of Levels and Experience
- [x] Calculation of experience for days of abstinence (+10 XP per day)
- [x] Penalty system when reassessing dependency after marking "I don't have this dependency" (-100 XP)
- [ ] Penalty system for relapses (-10 XP per day of relapse for 2+ consecutive days)
- [ ] Proper XP calculation for treatment completion based on dependency level (150, 350, 700 days)

## Notifications and Motivation
- [x] Daily motivational quote system with scheduling (basic implementation)
- [ ] Logic to send quotes only to active users who haven't accessed the site for more than 3 days
- [ ] Warning notification system for relapses

## Visual System
- [x] More sophisticated color transition algorithm based on XP progression (implemented in base.html)
- [x] Visual indicators for enlightenment level progression
- [x] Floating messages with close button in bottom-left corner

## Additional Functions
- [ ] Functionality for users to create their own dependencies (limited to 1 per user)
- [ ] Positive habits tracking system with XP rewards
- [ ] Donation button implementation
- [ ] Information about the project

## Pages Implementation
- [x] Dependency detail page with appropriate action buttons based on user state
- [ ] Calendar of abstinence for each dependency
- [ ] Settings for notifications page

## Business Logic
- [x] Complete XP calculation algorithm considering all factors (daily abstinence + dependency marking)
- [x] Level progression system with proper thresholds
- [ ] Notification scheduling and delivery system

## User Interface and Experience
- [x] Floating messages with close button in bottom-left corner
- [x] Fixed dependency detail page to show appropriate buttons based on user state
- [x] Prevented users from marking "I don't have this dependency" after starting treatment
- [x] Prevented users from changing dependency level once set
- [x] Removed all action buttons after user sets dependency level
- [x] Removed all action buttons after user marks "I don't have this dependency"
- [x] Implemented penalty system (100 XP deduction) when user wants to reassess dependency after marking "I don't have this dependency"

## User Scenarios
- [x] Complete implementation for "New user" scenario (registration, dependency selection)
- [x] Complete implementation for "Active user" scenario (daily marking, level progression)
- [ ] Complete implementation for "User with relapse" scenario

## Social Features
- [ ] Achievement and reward system

## Mobile Version
- [ ] Responsive design optimization
- [ ] Push notification system
- [ ] Offline mode for marking days

## Analytics
- [ ] Statistics by dependencies
- [ ] User progress statistics
- [ ] Treatment effectiveness analytics

## Administrative Panel
- [ ] Management of dependencies
- [ ] User statistics management
- [ ] Quote management
- [ ] Level system configuration