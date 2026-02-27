const express = require('express');
const app = express();
const port = 80;

// 模拟数据库数据
const mockData = {
    news: [
        {
            id: 1,
            title: "年初民航运输市场开局平稳，增长良好",
            url: "http://www.caacnews.com.cn/tt/202503/t20250318_1385950.html"
        },
        {
            id: 2,
            title: "民航局召开3月航空安全委员会全体（扩大）会议",
            url: "http://www.caacnews.com.cn/tt/202503/t20250314_1385858.html"
        },
        // 更多新闻数据...
    ],
    alumniStories: [
        {
            id: 1,
            content: "屈昊橙 2018 年进入中国民航大学，开启飞行生涯。在内蒙古飞行学院训练中，他驾驶多种机型完成从理论到实践的蜕变，积累了飞行经验。毕业后进入国航天津分公司，抓住 ACPC 课程机会，跳过高性能训练，直接进入模拟机训练，完成波音 737 初始改装训练，成为副驾驶。从校园到航空公司，他经历了从散漫到紧张、从飞行训练到航班生产的转变，感受到商业飞行与航校训练的巨大差异。凭借过硬技术和扎实理论基础，他应对了大型客机复杂系统和多变飞行环境的挑战。屈昊橙深知飞行员职业不仅是技术提升，更是心态和习惯养成，总结出过硬作风、胆大心细、严守规章、终身学习和保持平常心等习惯，助力他在飞行领域前行。"
        },
        {
            id: 2,
            content: "张彭叙从中国民航大学毕业后投身蓝天，每一步都坚实有力。刚入学时，他感到迷茫，但通过军训和社团活动逐渐适应，担任飞院舞协会长，丰富了大学生活。他提醒学弟学妹们，未来按部就班，珍惜学习机会。在大学期间，张彭叙重视理论学习，从零开始掌握专业知识，强调理论知识对飞行的基础作用。经过两年理论学习，他通过私商仪考试，进入航校进行飞行训练。在训练中，他体验了飞行的魅力和挑战，如练习失速改出时的失重感。他鼓励学弟学妹们学好飞行本领，保持冷静，确保安全。如今，张彭叙已成长为一名合格飞行员。他鼓励学弟学妹们相信国家民航实力，坚持梦想，不受负面言论影响，强调英语学习的重要性，建议多看英语影视作品，有计划地学习。"
        },

    ],
    careers: [
        {
            id: 1,
            name: "飞行员",
            description: "飞行员负责飞机的操作，包括起飞、飞行和降落，是航空安全的直接责任人。他们需要经过严格的训练，持有相应执照，并持续进行专业培训。",
            image: "1.jpg"
        },
        {
            id: 2,
            name: "机务维修人员",
            description: "机务维修人员负责飞机的维护、检查和修理，确保飞机的技术状态符合安全标准。机务人员的工作对飞行安全至关重要，需要高度的专业知识和责任感。",
            image: "2.jpg"
        },

    ]
};

// 定义API路由
app.get('', (req, res) => {
    try {
        res.json(mockData.news);
    } catch (error) {
        console.error('获取新闻数据失败:', error);
        res.status(500).json({ error: '获取新闻数据失败' });
    }
});

app.get('', (req, res) => {
    try {
        res.json(mockData.alumniStories);
    } catch (error) {
        console.error('获取校友故事失败:', error);
        res.status(500).json({ error: '获取校友故事失败' });
    }
});

app.get('', (req, res) => {
    try {
        res.json(mockData.careers);
    } catch (error) {
        console.error('获取热门职业数据失败:', error);
        res.status(500).json({ error: '获取热门职业数据失败' });
    }
});

// 启动服务器
app.listen(port, () => {
    console.log(`服务器运行在 http://localhost:${port}`);
});
