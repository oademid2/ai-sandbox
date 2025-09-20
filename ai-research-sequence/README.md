# AI Research Sequence: Automated Market Research Workflow

> **Transform market research from weeks to minutes with AI-powered automation**

## 📖 Blog Post: Building an AI-Powered Market Research Workflow

### Introduction

In today's fast-paced business environment, accurate market sizing is crucial for strategic decision-making. Traditional market research methods are often time-consuming, expensive, and require significant manual effort. This project demonstrates how AI can transform traditional market research workflows by automating the entire process from initial market description to final market size estimation.

### The Problem

Market sizing typically involves several complex steps:
1. **Clarification**: Understanding what exactly needs to be sized
2. **Formula Development**: Creating mathematical models to calculate market size
3. **Data Sourcing**: Finding reliable data sources for each component
4. **Synthesis**: Combining data points into final estimates

Each step requires domain expertise and significant research time. This project automates this entire workflow using AI.

### The Solution: AI Research Sequence

The system breaks down market research into three main phases:

#### Phase 1: Market Formula Generation
- Takes a simple market description (e.g., "edtech software management for teachers")
- Uses GPT-4 to generate clarifying questions
- Creates multiple market sizing formulas
- Identifies key components needed for each formula

#### Phase 2: Data Source Discovery
- Uses Exa API for semantic web search
- Automatically searches for relevant data sources
- Extracts numeric data points from web sources
- Synthesizes information into structured data

#### Phase 3: Market Size Calculation
- Combines all data points to calculate market size estimates
- Provides confidence intervals and sensitivity analysis

### Technical Architecture

#### Backend: AWS Lambda + Python
- **Serverless Architecture**: Deployed on AWS Lambda for scalability
- **AI Integration**: OpenAI GPT-4 for formula generation and data synthesis
- **Data Sourcing**: Exa API for semantic web search and data extraction
- **Prompt Engineering**: Structured prompt factory for consistent AI responses

#### Frontend: Next.js + TypeScript
- **Modern UI**: Built with Next.js 15, TypeScript, and Tailwind CSS
- **Component Library**: Shadcn/ui for consistent, accessible components
- **Real-time Updates**: Dynamic formula editing and data source selection
- **Responsive Design**: Works seamlessly across desktop and mobile devices

### Key Features

1. **Interactive Formula Editing**: Users can modify AI-generated formulas in real-time
2. **Data Source Validation**: Multiple sources for each component with confidence scoring
3. **Market Size Calculator**: Automatic calculation with sensitivity analysis
4. **Export Capabilities**: Results can be exported for further analysis

### Results and Impact

The system successfully automates what previously took days or weeks of manual research. For example, when testing with "edtech software management," the system:

- Generated 2 different market sizing formulas in seconds
- Identified 6 key components (number of schools, average software spend, etc.)
- Found 15+ data sources with actual numeric values
- Calculated a market size estimate of $2.1B with confidence intervals

---

## 🏗️ Technical Documentation

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External APIs │
│   (Next.js)     │◄──►│   (AWS Lambda)  │◄──►│   OpenAI + Exa  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

#### Backend
- **Runtime**: Python 3.9+ on AWS Lambda
- **AI Services**: OpenAI GPT-4, Exa API
- **Dependencies**: `exa_py`, `openai`, `requests`
- **Architecture**: Serverless with REST API

#### Frontend
- **Framework**: Next.js 15 with TypeScript
- **Styling**: Tailwind CSS + Shadcn/ui
- **State Management**: React hooks
- **Build Tool**: Vite (via Next.js)

### Core Workflow

1. **Market Description Input** → User provides market description
2. **Formula Generation** → AI creates market sizing formulas
3. **Component Decomposition** → Formula broken into data components
4. **Data Sourcing** → Exa API finds relevant data sources
5. **Market Size Calculation** → Final estimates with confidence intervals

### API Endpoints

#### GET /brainstorm
Generates market sizing formulas for a given market description.

**Parameters:**
- `action=brainstorm`
- `market_description` (string)

**Response:**
```json
{
  "formulas": ["formula1", "formula2", ...]
}
```

#### GET /decompose
Breaks down a formula into individual components.

**Parameters:**
- `action=decompose`
- `formula` (string)

**Response:**
```json
{
  "components": ["component1", "component2", ...]
}
```

#### POST /datasource
Finds data sources for given components.

**Body:**
```json
{
  "components": ["component1", "component2", ...]
}
```

**Response:**
```json
{
  "datasources": {
    "component1": [...],
    "component2": [...]
  }
}
```

### Key Classes and Functions

#### ResearchSequenceTask
Main class handling the AI workflow.

**Key Methods:**
- `generate_market_formulas(market_description)`: Creates market sizing formulas
- `get_components_from_formula(formula)`: Decomposes formulas into components
- `run_exa_workflow_for_components_sequential(components)`: Sources data for components

#### PromptFactory
Manages structured prompts for consistent AI interactions.

**Available Prompts:**
- `clarifying_questions_prompt`
- `formula_brainstorm_prompt`
- `datasource_prompt`
- `exa_synthesis_prompt`
- `decompose_formula_prompt`

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- AWS Account (for Lambda deployment)
- OpenAI API Key
- Exa API Key

### Backend Setup

1. **Clone and Setup Environment**
```bash
cd ai-research-sequence
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure Environment Variables**
```bash
export OPENAI_API_KEY=your_openai_api_key
export EXA_API_KEY=your_exa_api_key
```

3. **Deploy to AWS Lambda**
```bash
# Package the application
zip -r lambda_function.zip lambda/ requirements.txt

# Deploy using AWS CLI or console
aws lambda create-function \
  --function-name ai-research-sequence \
  --runtime python3.9 \
  --handler lambda.lambda_function.lambda_handler \
  --zip-file fileb://lambda_function.zip
```

### Frontend Setup

1. **Install Dependencies**
```bash
cd research-sequence-ui
npm install
```

2. **Configure Environment**
```bash
# Create .env.local
NEXT_PUBLIC_API_URL=your_lambda_function_url
```

3. **Run Development Server**
```bash
npm run dev
```

4. **Build for Production**
```bash
npm run build
npm start
```

---

## 📁 Project Structure

```
ai-research-sequence/
├── lambda/                          # Backend Lambda functions
│   ├── lambda_function.py           # Main Lambda handler
│   ├── research_sequence_task.py    # Core AI workflow logic
│   ├── prompt_factory.py            # Structured prompt management
│   └── test/                        # Test files
├── 0 _Use Case Script.ipynb         # Initial prototyping
├── 1 _ Standardize Script.ipynb     # Standardized workflow
├── deploy_debug_lambda.py           # Deployment utilities
├── package_aws.py                   # AWS packaging script
├── requirements.txt                 # Python dependencies
└── README.md                        # This file

research-sequence-ui/
├── app/                             # Next.js app directory
│   ├── page.tsx                     # Main application page
│   ├── layout.tsx                   # Root layout
│   └── globals.css                  # Global styles
├── components/                      # React components
│   ├── ui/                          # Shadcn/ui components
│   └── theme-provider.tsx           # Theme configuration
├── lib/                             # Utility functions
├── hooks/                           # Custom React hooks
├── public/                          # Static assets
├── package.json                     # Node.js dependencies
└── tailwind.config.ts              # Tailwind configuration
```

---

## 🔧 Development

### Backend Development

The backend is built using a modular approach:

1. **ResearchSequenceTask**: Main workflow orchestrator
2. **PromptFactory**: Manages AI prompts for consistency
3. **Lambda Handler**: HTTP API endpoint handler

### Frontend Development

The frontend follows modern React patterns:

1. **Server Components**: Next.js 13+ app directory structure
2. **Client Components**: Interactive elements with React hooks
3. **UI Components**: Reusable Shadcn/ui components
4. **State Management**: React hooks for local state

### Testing

#### Backend Testing
- Use Jupyter notebooks for prompt testing
- Test Lambda function with sample events
- Validate API responses

#### Frontend Testing
- Test formula editing functionality
- Validate data source selection
- Check market size calculations

---

## 🔒 Security & Performance

### Security Considerations

- **API Keys**: Stored securely in environment variables
- **CORS**: Configured for cross-origin requests
- **Input Validation**: All user inputs are validated
- **Rate Limiting**: Implemented to prevent API abuse

### Performance Optimizations

- **Parallel Processing**: Data extraction runs in parallel
- **Caching**: Consider Redis for frequently accessed data
- **Error Handling**: Comprehensive error handling for API failures
- **Monitoring**: CloudWatch integration for performance tracking

---

## 📊 Monitoring & Logging

### Backend Monitoring
- **CloudWatch**: Monitor Lambda function performance
- **Error Tracking**: Log all API errors and exceptions
- **Usage Analytics**: Track API usage patterns

### Frontend Monitoring
- **Error Boundaries**: React error boundaries for graceful failures
- **Performance Metrics**: Core Web Vitals tracking
- **User Analytics**: Usage pattern analysis

---

## 🚀 Deployment

### Backend Deployment (AWS Lambda)

1. **Package Application**
```bash
cd ai-research-sequence
zip -r lambda_function.zip lambda/ requirements.txt
```

2. **Deploy to Lambda**
```bash
aws lambda update-function-code \
  --function-name ai-research-sequence \
  --zip-file fileb://lambda_function.zip
```

3. **Configure Environment Variables**
```bash
aws lambda update-function-configuration \
  --function-name ai-research-sequence \
  --environment Variables='{OPENAI_API_KEY=your_key,EXA_API_KEY=your_key}'
```

### Frontend Deployment (Vercel)

1. **Connect Repository**
```bash
# Connect your GitHub repository to Vercel
# Configure environment variables in Vercel dashboard
```

2. **Deploy**
```bash
# Vercel will automatically deploy on push to main branch
git push origin main
```

---

## 🔮 Future Enhancements

### Planned Features

1. **Data Validation**
   - Confidence scoring for data sources
   - Automated data quality assessment
   - Source credibility ratings

2. **Advanced Analytics**
   - Historical data analysis
   - Trend identification
   - Market growth projections

3. **Competitive Intelligence**
   - Competitor analysis integration
   - Market share calculations
   - Competitive positioning insights

4. **Enhanced Reporting**
   - PDF report generation
   - Customizable report templates
   - Data visualization improvements

5. **User Management**
   - User authentication
   - Saved research projects
   - Collaboration features

6. **API Enhancements**
   - GraphQL API
   - Webhook support
   - Real-time updates

### Technical Improvements

1. **Performance**
   - Redis caching layer
   - CDN integration
   - Database optimization

2. **Scalability**
   - Microservices architecture
   - Load balancing
   - Auto-scaling

3. **Reliability**
   - Circuit breakers
   - Retry mechanisms
   - Fallback strategies

---

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests**
5. **Submit a pull request**

### Code Standards

- **Python**: Follow PEP 8 guidelines
- **TypeScript**: Use strict mode and proper typing
- **React**: Follow React best practices
- **Documentation**: Update docs for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI**: For providing the GPT-4 API
- **Exa**: For semantic search capabilities
- **AWS**: For serverless infrastructure
- **Vercel**: For frontend hosting
- **Shadcn/ui**: For the component library

---

## 📞 Support

For questions, issues, or contributions:

1. **Issues**: Create an issue on GitHub
2. **Discussions**: Use GitHub Discussions
3. **Email**: [Your Email]

---

*Last updated: December 2024* 